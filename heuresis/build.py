"""src/sections/*.html 조각을 순서대로 이어 붙여 heuresis-vol01.html을 만든다"""
import glob, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from typo import polish
here = os.path.dirname(os.path.abspath(__file__))
HEAD = open(os.path.join(here, 'src', 'head.html')).read()

def wrap(body):
    return HEAD + '<body>\n' + polish(body) + '\n<script src="heuresis-art.js"></script>\n</body>\n</html>\n'

if __name__ == '__main__':
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(here, 'src', 'sections', '*.html')))
    body = '\n'.join(open(f).read() for f in files)
    out = os.environ.get('OUT', os.path.join(here, 'heuresis-vol01.html'))
    open(out, 'w').write(wrap(body))
    print(out, len(files), 'sections')
