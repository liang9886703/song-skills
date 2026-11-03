#!/usr/bin/env python3
"""读取旧内网技能目录及包地址；不安装、不覆盖任何技能。"""
import argparse
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.parse
import urllib.request


class CatalogError(Exception):
    pass


def resolve_base_url(config=None):
    value = os.environ.get('SKILL_INTERNAL_CATALOG_URL', '')
    if not value:
        config_path = Path(config) if config else Path(
            os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config'))
        ) / 'skillshare' / 'discovery.json'
        try:
            value = json.loads(config_path.read_text()).get('internal_catalog_base_url', '')
        except FileNotFoundError:
            raise CatalogError('provider_not_configured') from None
        except (ValueError, OSError, AttributeError):
            raise CatalogError('invalid_provider_config') from None
    if not isinstance(value, str) or not value:
        raise CatalogError('provider_not_configured')
    try:
        url = urllib.parse.urlsplit(value)
    except ValueError:
        raise CatalogError('invalid_provider_url') from None
    if url.scheme not in ('http', 'https') or not url.hostname or url.username or url.password or url.query or url.fragment:
        raise CatalogError('invalid_provider_url')
    return value.rstrip('/')


def fetch(command, identifier=None, config=None):
    base = resolve_base_url(config)
    if command == 'list':
        url = base + '/api/v1/skills/metadata'
    elif command == 'url' and identifier:
        url = base + '/api/v1/skills/package?' + urllib.parse.urlencode({'skillIdentifier': identifier})
    else:
        raise CatalogError('invalid_command')
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            payload = json.loads(response.read().decode('utf-8'))
    except (urllib.error.URLError, TimeoutError, OSError):
        raise CatalogError('provider_unavailable') from None
    except (ValueError, UnicodeError):
        raise CatalogError('invalid_provider_response') from None
    if not isinstance(payload, dict) or payload.get('code') != 200:
        raise CatalogError('provider_error')
    data = payload.get('data')
    if command == 'list':
        if data is None:
            return []
        if not isinstance(data, list):
            raise CatalogError('invalid_catalog_shape')
        return data
    package_url = data.get('bosUrl') if isinstance(data, dict) else None
    if not isinstance(package_url, str) or not package_url:
        raise CatalogError('package_url_missing')
    try:
        parsed = urllib.parse.urlsplit(package_url)
    except ValueError:
        raise CatalogError('invalid_package_url') from None
    if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password:
        raise CatalogError('invalid_package_url')
    return {'identifier': identifier, 'package_url': package_url}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', help='私有 discovery.json 路径；默认使用 skillshare 配置目录')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('list', help='读取目录，不安装')
    url = sub.add_parser('url', help='读取指定技能的包地址，不下载')
    url.add_argument('identifier')
    args = parser.parse_args()
    try:
        data = fetch(args.command, getattr(args, 'identifier', None), args.config)
    except CatalogError as error:
        print(json.dumps({'provider': 'legacy-internal', 'success': False, 'error': str(error)}))
        return 1
    print(json.dumps({'provider': 'legacy-internal', 'success': True, 'data': data}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
