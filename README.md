# Model Output Gate

AI-security educational prototype for treating generated output as untrusted text. Initial code was AI-assisted. It escapes HTML text and link labels, and allows clickable links only for explicitly listed exact HTTPS hostnames. No browser, model or network call is made by the CLI.

```sh
python output_gate.py example.json --allow-host example.com
python -m unittest -v
```

The fictional example returns 1 because one link is withheld. Exit 0 means rendering completed without withheld links, not safe content. Exit 2 is input error. Output is a JSON object containing an HTML fragment and withheld-link count. The HTML uses escaped text in a pre element; it does not parse Markdown or permit model-supplied markup. Default link allowlist is empty. Host matching is exact, not suffix based.

## Limits

This is output encoding for a specific HTML-text/quoted-href context, not a general sanitizer or DLP system. It does not detect misinformation, secrets, harmful advice, phishing on an allowed host or prompt injection. It does not fetch URLs, resolve redirects, check DNS, prevent server-side request forgery or control navigation after a click. An allowed host may host untrusted pages. If adapting this for a web app, retain the exact encoding context and add appropriate browser policies, accessibility and review. Do not pass its result into script, style or other contexts. Input may contain sensitive data: keep real inputs and outputs private. Size limits apply after JSON loading; this is not a hostile-input service. No production-readiness claim.

Python 3.9+ is an intended compatibility target. Verification is assistant-run, not Dahoba's personal execution. CI run pages, if present, are the source for actual CI results. See GUIDE_AR.md.

Reference: https://genai.owasp.org/llm-top-10/ (improper output handling and sensitive information disclosure).
