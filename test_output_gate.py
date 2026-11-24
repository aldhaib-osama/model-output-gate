import unittest
from output_gate import allowed_url,render
class GateTests(unittest.TestCase):
    def test_script_is_text(self):
        r=render({'text':'<script>alert(1)</script>'},set())
        self.assertNotIn('<script>',r['html']);self.assertIn('&lt;script&gt;',r['html'])
    def test_html_label_escaped(self):
        r=render({'text':'ok','links':[{'label':'<img onerror=x>','url':'https://example.com'}]}, {'example.com'})
        self.assertNotIn('<img',r['html'])
    def test_allowed_https(self):self.assertTrue(allowed_url('https://example.com/path',{'example.com'}))
    def test_suffix_not_allowed(self):self.assertFalse(allowed_url('https://example.com.evil.invalid',{'example.com'}))
    def test_userinfo_denied(self):self.assertFalse(allowed_url('https://user@example.com',{'example.com'}))
    def test_script_scheme_denied(self):self.assertFalse(allowed_url('javascript:alert(1)',set()))
    def test_http_denied(self):self.assertFalse(allowed_url('http://example.com',{'example.com'}))
    def test_bad_port_denied(self):self.assertFalse(allowed_url('https://example.com:bad',{'example.com'}))
    def test_whitespace_denied(self):self.assertFalse(allowed_url('https://example.com/\nfoo',{'example.com'}))
    def test_default_denies_links(self):self.assertEqual(render({'text':'ok','links':[{'label':'x','url':'https://example.com'}]},set())['blocked_links'],1)
    def test_unknown_field(self):
        with self.assertRaises(ValueError):render({'text':'x','script':'x'},set())
    def test_large_input(self):
        with self.assertRaises(ValueError):render({'text':'x'*10001},set())
if __name__=='__main__':unittest.main()
