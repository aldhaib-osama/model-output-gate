"""Render untrusted generated text as escaped HTML text, never executable markup."""
import argparse
import html
import json
from urllib.parse import urlsplit


def allowed_url(value, allowed_hosts):
    if not isinstance(value,str) or not value or any(ord(c)<33 for c in value):
        return False
    try:
        url=urlsplit(value)
        return (url.scheme == 'https' and url.hostname in allowed_hosts
                and url.username is None and url.password is None
                and url.port in (None,443))
    except ValueError:
        return False


def render(data, allowed_hosts):
    if not isinstance(data,dict) or set(data)-{'text','links'}:
        raise ValueError('Expected only text and optional links')
    body=data.get('text'); links=data.get('links',[])
    if not isinstance(body,str) or len(body)>10000 or not isinstance(links,list) or len(links)>20:
        raise ValueError('Invalid content or size limit exceeded')
    rendered=['<article><pre>'+html.escape(body,quote=True)+'</pre>']
    blocked=0
    for link in links:
        if not isinstance(link,dict) or set(link)!={'label','url'} or not isinstance(link['label'],str):
            raise ValueError('Malformed link')
        if len(link['label'])>200 or not isinstance(link['url'],str) or len(link['url'])>2048:
            raise ValueError('Invalid link size or type')
        if allowed_url(link['url'],allowed_hosts):
            rendered.append('<a rel="noopener noreferrer" href="'+html.escape(link['url'],quote=True)+'">'+html.escape(link['label'])+'</a>')
        else:
            blocked+=1
            rendered.append('<span>'+html.escape(link['label'])+' [link withheld]</span>')
    rendered.append('</article>')
    return {'html':'\n'.join(rendered),'blocked_links':blocked}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input');parser.add_argument('--allow-host',action='append',default=[])
    args=parser.parse_args(argv)
    try:
        with open(args.input,encoding='utf-8') as f:data=json.load(f)
        result=render(data,set(args.allow_host))
        print(json.dumps(result,indent=2));return 1 if result['blocked_links'] else 0
    except (OSError,ValueError) as e:parser.exit(2,f'Input error: {e}\n')
if __name__=='__main__':raise SystemExit(main())
