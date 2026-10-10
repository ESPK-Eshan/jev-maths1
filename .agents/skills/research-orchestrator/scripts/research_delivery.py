#!/usr/bin/env python3
"""Offline archive and delivery-record checks. Never calls a provider or replays jobs."""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import unicodedata
import zipfile


class ContractError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ContractError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'), object_pairs_hook=unique_object,
                      parse_constant=lambda value: (_ for _ in ()).throw(ContractError('nonfinite JSON value: ' + value)))


def digest_file(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def safe_name(name):
    require(isinstance(name, str) and name, 'empty/nonstring archive path')
    require('\\' not in name and not name.startswith('/') and '\x00' not in name, 'unsafe path: ' + name)
    parts = name.split('/')
    require(all(part and part not in ('.', '..') for part in parts), 'relative traversal/empty component: ' + name)
    reserved = {'CON', 'PRN', 'AUX', 'NUL', *(f'COM{i}' for i in range(1, 10)), *(f'LPT{i}' for i in range(1, 10))}
    for part in parts:
        require(not any(ord(c) < 32 or c in '<>:"|?*' for c in part), 'nonportable path component: ' + part)
        require(not part.endswith((' ', '.')), 'nonportable trailing character: ' + part)
        require(part.split('.')[0].upper() not in reserved, 'reserved device path: ' + part)
    return unicodedata.normalize('NFC', name).casefold()


def hash_value(value):
    require(isinstance(value, str) and re.fullmatch('[0-9a-fA-F]{64}', value), 'invalid SHA-256')
    return value.lower()


def bound_path(root, name):
    safe_name(name)
    root = Path(root).resolve()
    path = root.joinpath(*PurePosixPath(name).parts)
    require(not any(part.is_symlink() for part in (path, *path.parents) if part != root.parent), 'symlink path is unsupported')
    resolved = path.resolve()
    require(resolved.is_relative_to(root), 'path escapes supplied root')
    return resolved


def verify_archive(archive, manifest, extract_to=None, max_bytes=10 * 1024**3):
    """Verify exact manifest bytes before optional extraction into a new directory.

    Exclusion reasons are retained but this does not discover omissions from the source
    project or detect secrets. The coordinator must independently audit that inventory.
    """
    require(type(max_bytes) is int and max_bytes >= 0, 'max_bytes must be a nonnegative integer')
    require(isinstance(manifest, dict) and type(manifest.get('schema_version')) is int and manifest['schema_version'] == 1, 'unsupported manifest schema')
    entries = manifest.get('files')
    require(isinstance(entries, list) and entries, 'manifest needs at least one file')
    expected, names = {}, set()
    for item in entries:
        require(isinstance(item, dict), 'file descriptor must be object')
        name = item.get('path')
        key = safe_name(name)
        require(key not in names, 'duplicate/colliding manifest path: ' + name)
        names.add(key)
        require(type(item.get('bytes')) is int and item['bytes'] >= 0, 'invalid byte count')
        expected[name] = (item['bytes'], hash_value(item.get('sha256')))
    exclusions = manifest.get('exclusions', [])
    require(isinstance(exclusions, list), 'exclusions must be list')
    for item in exclusions:
        require(isinstance(item, dict) and isinstance(item.get('reason'), str) and item['reason'].strip(), 'exclusion needs a reason')
        require(safe_name(item.get('path')) not in names, 'excluded path also included')
    require(sum(size for size, _ in expected.values()) <= max_bytes, 'declared inventory exceeds extraction budget')
    if extract_to is not None:
        require(not Path(extract_to).exists() and not Path(extract_to).is_symlink(), 'extraction requires a new destination')
    with zipfile.ZipFile(archive, 'r') as zipped:
        actual, canonical, kinds = {}, set(), {}
        for entry in zipped.infolist():
            name = entry.filename[:-1] if entry.is_dir() else entry.filename
            key = safe_name(name)
            require(key not in canonical, 'duplicate/colliding ZIP entry: ' + name)
            canonical.add(key)
            mode = entry.external_attr >> 16
            require(not stat.S_ISLNK(mode), 'symlink ZIP entry is unsupported')
            require(not entry.flag_bits & 1, 'encrypted ZIP entry unsupported')
            require(stat.S_IFMT(mode) in (0, stat.S_IFREG, stat.S_IFDIR), 'special ZIP entry unsupported')
            kinds[key] = 'directory' if entry.is_dir() else 'file'
            if not entry.is_dir():
                actual[name] = entry
        for key in kinds:
            for parent in PurePosixPath(key).parents:
                require(kinds.get(str(parent)) != 'file', 'file collides with directory ancestor')
        require(set(actual) == set(expected), 'ZIP file inventory differs from manifest')
        require(sum(item.file_size for item in actual.values()) <= max_bytes, 'ZIP exceeds extraction budget')
        for name, entry in actual.items():
            wanted_size, wanted_hash = expected[name]
            require(entry.file_size == wanted_size, 'size mismatch: ' + name)
            size, digest = 0, hashlib.sha256()
            with zipped.open(entry, 'r') as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                    size += len(chunk)
                    require(size <= wanted_size, 'expanded content exceeds declaration: ' + name)
                    digest.update(chunk)
            require(size == wanted_size and digest.hexdigest() == wanted_hash, 'content hash mismatch: ' + name)
        if extract_to is not None:
            destination = Path(extract_to).absolute()
            destination.mkdir(parents=False, exist_ok=False)
            # No extractall: every name was checked and every file is opened exclusively.
            for name, entry in actual.items():
                path = bound_path(destination, name)
                path.parent.mkdir(parents=True, exist_ok=True)
                with zipped.open(entry, 'r') as source, path.open('xb') as target:
                    digest, size = hashlib.sha256(), 0
                    for chunk in iter(lambda: source.read(1024 * 1024), b''):
                        size += len(chunk)
                        require(size <= expected[name][0], 'changed source during extraction')
                        target.write(chunk)
                        digest.update(chunk)
                require(size == expected[name][0] and digest.hexdigest() == expected[name][1], 'changed source during extraction')
    return {'status': 'verified-local-content', 'files': len(expected), 'bytes': sum(size for size, _ in expected.values()),
            'archive_sha256': digest_file(archive), 'exclusions': exclusions, 'extracted_to': str(extract_to) if extract_to else None,
            'source_inventory_independently_audited': False, 'secret_audit_performed': False}


def timestamp(value):
    require(isinstance(value, str), 'timestamp is required')
    try:
        result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError as exc:
        raise ContractError('invalid ISO timestamp') from exc
    require(result.utcoffset() is not None, 'timestamp needs timezone')
    return result


def verify_reference(root, item):
    require(isinstance(item, dict), 'reference must be object')
    path = bound_path(root, item.get('path'))
    require(path.is_file(), 'missing referenced file: ' + str(path))
    require(digest_file(path) == hash_value(item.get('sha256')), 'reference content changed: ' + str(path))
    return path


def verify_delivery(root, index, acknowledgment=None):
    """Validate supplied record chain, never authenticate or contact remote storage.

    A missing/mismatched closing record conservatively yields delivery-pending. Actual
    accepted stage transitions still use research_state and independent reviewer receipts.
    """
    report = {'status': 'delivery-pending', 'valid_segments': 0, 'reasons': [], 'remote_independently_attested': False,
              'historical_actions_replayed': False}
    try:
        require(isinstance(index, dict) and type(index.get('schema_version')) is int and index['schema_version'] == 1, 'unsupported delivery-index schema')
        identity = {k: index.get(k) for k in ('project_id', 'run_id', 'delivery_version')}
        require(all(isinstance(identity[k], str) and identity[k] for k in ('project_id', 'run_id')), 'missing delivery identity')
        require(type(identity['delivery_version']) is int and identity['delivery_version'] >= 1, 'invalid delivery version')
        base = index.get('base')
        verify_reference(root, base)
        base_hash = hash_value(base['sha256'])
        previous = base_hash
        segments = index.get('segments')
        require(isinstance(segments, list) and segments, 'closing supplement list is required')
        seen_paths, segment_times, all_hashes = {safe_name(base['path'])}, [], [base_hash]
        for position, descriptor in enumerate(segments, 1):
            require(isinstance(descriptor, dict), 'invalid segment descriptor')
            require(type(descriptor.get('sequence')) is int and descriptor['sequence'] == position, 'nonconsecutive segment sequence')
            require(hash_value(descriptor.get('previous_sha256')) == previous, 'segment predecessor mismatch')
            key = safe_name(descriptor.get('path'))
            require(key not in seen_paths, 'repeated delivery path')
            seen_paths.add(key)
            segment = read_json(verify_reference(root, descriptor))
            require(isinstance(segment, dict), 'segment must be a JSON object')
            require(type(segment.get('schema_version')) is int and segment['schema_version'] == 1, 'unsupported segment schema')
            require(all(segment.get(k) == v and type(segment.get(k)) is type(v) for k, v in identity.items()), 'segment identity mismatch')
            require(type(segment.get('sequence')) is int and segment['sequence'] == position, 'segment sequence mismatch')
            require(hash_value(segment.get('base_sha256')) == base_hash and hash_value(segment.get('previous_sha256')) == previous, 'segment binding mismatch')
            require(segment.get('state') in ('recording', 'acceptance-ready', 'limitation'), 'uploaded segment cannot assert final acceptance')
            moment = timestamp(segment.get('created_at'))
            require(not segment_times or moment >= segment_times[-1], 'segment timestamps out of order')
            segment_times.append(moment)
            previous = hash_value(descriptor['sha256'])
            all_hashes.append(previous)
            report['valid_segments'] = position
        require(segment.get('state') == 'acceptance-ready', 'last supplement is not acceptance-ready')
        reviews = segment.get('stage22_reviews')
        require(isinstance(reviews, list) and reviews, 'closing supplement needs review references')
        for review in reviews:
            verify_reference(root, review)
        require(acknowledgment is not None, 'terminal local acknowledgment is missing; readiness is not acceptance')
        ack = acknowledgment
        require(isinstance(ack, dict) and type(ack.get('schema_version')) is int and ack['schema_version'] == 1, 'unsupported acknowledgment schema')
        require(all(ack.get(k) == v and type(ack.get(k)) is type(v) for k, v in identity.items()), 'acknowledgment identity mismatch')
        require(ack.get('status') == 'delivered' and ack.get('stage22_status') == 'accepted', 'acknowledgment is not final acceptance')
        require(hash_value(ack.get('base_sha256')) == base_hash and hash_value(ack.get('last_segment_sha256')) == previous, 'acknowledgment artifact binding mismatch')
        accepted_at = timestamp(ack.get('verified_at'))
        proofs = ack.get('content_verifications')
        require(isinstance(proofs, list), 'content-verification receipts are required')
        verified = set()
        for proof in proofs:
            require(isinstance(proof, dict), 'invalid verification record')
            artifact_hash = hash_value(proof.get('artifact_sha256'))
            require(artifact_hash in all_hashes and artifact_hash not in verified, 'duplicate/unrelated content verification')
            require(proof.get('method') in ('checksum', 'full-content-readback'), 'metadata-only verification is insufficient')
            verify_reference(root, proof.get('evidence'))
            checked_at = timestamp(proof.get('verified_at'))
            artifact_index = all_hashes.index(artifact_hash)
            require(checked_at <= accepted_at, 'acceptance predates content verification')
            require(artifact_index == 0 or checked_at >= segment_times[artifact_index - 1], 'verification predates supplement creation')
            verified.add(artifact_hash)
        require(verified == set(all_hashes), 'base or supplement content proof is missing')
        report['status'] = 'recorded-delivery-supported'
        report['verified_at'] = ack['verified_at']
        report['notice'] = 'Local bindings validated; independent reviewers must inspect actual service receipts and stage gates.'
    except (ContractError, OSError, ValueError, KeyError, TypeError) as exc:
        report['reasons'].append(str(exc))
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    archive = sub.add_parser('archive-verify', help='Verify a ZIP against its full declared inventory')
    archive.add_argument('archive', type=Path)
    archive.add_argument('--manifest', type=Path, required=True)
    archive.add_argument('--extract-to', type=Path)
    archive.add_argument('--max-bytes', type=int, default=10 * 1024**3)
    chain = sub.add_parser('delivery-verify', help='Check frozen-base/supplement/terminal-acknowledgment records')
    chain.add_argument('root', type=Path)
    chain.add_argument('--index', type=Path, required=True)
    chain.add_argument('--ack', type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == 'archive-verify':
            result = verify_archive(args.archive, read_json(args.manifest), args.extract_to, args.max_bytes)
        else:
            result = verify_delivery(args.root, read_json(args.index), read_json(args.ack) if args.ack else None)
        print(json.dumps(result, indent=2))
        return 3 if result['status'] == 'delivery-pending' else 0
    except (ContractError, OSError, ValueError, zipfile.BadZipFile, RuntimeError) as exc:
        print(json.dumps({'status': 'invalid', 'error': str(exc)}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
