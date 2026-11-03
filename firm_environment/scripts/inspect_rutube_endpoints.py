import urllib.request
import re

def main():
    req = urllib.request.Request('https://studio.rutube.ru/videos/', headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        scripts = re.findall(r'src="([^"]+\.js)"', html)
        print('Found scripts count:', len(scripts))
        for s in scripts:
            if not s.startswith('http'):
                s = 'https://studio.rutube.ru' + s
            try:
                js = urllib.request.urlopen(urllib.request.Request(s, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8', errors='ignore')
                endpoints = re.findall(r'"(/api/[^"]+)"', js)
                uploader_matches = [e for e in set(endpoints) if 'upload' in e or 'video' in e or 'batch' in e]
                if uploader_matches:
                    print('Endpoints in', s.split('/')[-1], uploader_matches[:10])
            except Exception as ex:
                pass
    except Exception as e:
        print('Error:', e)

if __name__ == '__main__':
    main()
