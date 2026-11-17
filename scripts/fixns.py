import re, os
os.chdir(os.path.expanduser('~/aospa'))
files = ['vendor/motorola/rtwo/Android.bp', 'vendor/motorola/sm8550-common/Android.bp']
for f in files:
    s = open(f).read()
    m = re.search(r'imports: \[(.*?)\]', s, re.S)
    items = re.findall(r'"([^"]+)"', m.group(1))
    keep = []
    for p in items:
        bp = os.path.join(p, 'Android.bp')
        ok = os.path.isfile(bp) and 'soong_namespace' in open(bp).read()
        print(f, p, 'OK' if ok else 'QUITAR')
        if ok:
            keep.append(p)
    new = 'imports: [\n' + ''.join('        "%s",\n' % p for p in keep) + '    ]'
    s = s[:m.start()] + new + s[m.end():]
    open(f, 'w').write(s)
