import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.parse
import urllib.error

spec = importlib.util.spec_from_file_location('internal_catalog', Path(__file__).with_name('internal_catalog.py'))
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(catalog.os.environ, {'SKILL_INTERNAL_CATALOG_URL': 'https://catalog.example'}, clear=True)
        self.env.start()
        self.addCleanup(self.env.stop)

    def respond(self, payload):
        return patch.object(catalog.urllib.request, 'urlopen', return_value=io.BytesIO(json.dumps(payload).encode()))

    def test_list_and_empty_result(self):
        with self.respond({'code': 200, 'data': [{'name': 'demo'}]}):
            self.assertEqual(catalog.fetch('list'), [{'name': 'demo'}])
        with self.respond({'code': 200, 'data': None}):
            self.assertEqual(catalog.fetch('list'), [])

    def test_identifier_is_encoded_without_injecting_parameters(self):
        identifier = '中文 skill&a=b/?'
        with self.respond({'code': 200, 'data': {'bosUrl': 'https://package.example/demo.zip'}}) as request:
            result = catalog.fetch('url', identifier)
        url = request.call_args.args[0]
        self.assertEqual(urllib.parse.parse_qs(urllib.parse.urlsplit(url).query), {'skillIdentifier': [identifier]})
        self.assertEqual(result['identifier'], identifier)
        self.assertEqual(request.call_args.kwargs['timeout'], 10)

    def test_config_and_missing_config(self):
        with patch.dict(catalog.os.environ, {}, clear=True), tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'discovery.json'
            with self.assertRaisesRegex(catalog.CatalogError, '^provider_not_configured$'):
                catalog.resolve_base_url(p)
            p.write_text(json.dumps({'internal_catalog_base_url': 'https://configured.example/'}))
            self.assertEqual(catalog.resolve_base_url(p), 'https://configured.example')

    def test_remote_failure_does_not_expose_response_or_credentials(self):
        with self.respond({'code': 403, 'message': 'private response'}):
            with self.assertRaisesRegex(catalog.CatalogError, '^provider_error$'):
                catalog.fetch('list')
        with patch.object(catalog.urllib.request, 'urlopen', side_effect=urllib.error.URLError('private network details')):
            with self.assertRaisesRegex(catalog.CatalogError, '^provider_unavailable$'):
                catalog.fetch('list')

    def test_wrong_shapes_and_urls_fail(self):
        for command, payload, error in [
            ('list', {'code': 200, 'data': {}}, 'invalid_catalog_shape'),
            ('url', {'code': 200, 'data': {}}, 'package_url_missing'),
            ('url', {'code': 200, 'data': {'bosUrl': 'file:///tmp/x.zip'}}, 'invalid_package_url'),
            ('url', {'code': 200, 'data': {'bosUrl': 'https://[invalid'}}, 'invalid_package_url'),
        ]:
            with self.respond(payload), self.assertRaisesRegex(catalog.CatalogError, '^' + error + '$'):
                catalog.fetch(command, 'demo')
        for url in ['https://user:secret@catalog.example', 'https://[invalid']:
            with patch.dict(catalog.os.environ, {'SKILL_INTERNAL_CATALOG_URL': url}):
                with self.assertRaisesRegex(catalog.CatalogError, '^invalid_provider_url$'):
                    catalog.fetch('list')


if __name__ == '__main__':
    unittest.main()
