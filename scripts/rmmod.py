import sys, os, re
os.chdir(os.path.expanduser('~/aospa'))
name = sys.argv[1]
for bp in ['vendor/motorola/rtwo/Android.bp', 'vendor/motorola/sm8550-common/Android.bp']:
    s = open(bp).read()
    pat = re.compile(r'\n(cc_prebuilt_\w+|prebuilt_\w+)\s*\{\s*\n\s*name: "' + re.escape(name) + '",')
    m = pat.search(s)
    if not m:
        continue
    i = s.index('{', m.start())
    depth = 0
    for j in range(i, len(s)):
        depth += (s[j] == '{') - (s[j] == '}')
        if depth == 0:
            break
    open(bp, 'w').write(s[:m.start()] + s[j+1:])
    print('quitado de', bp)
for mk in ['vendor/motorola/rtwo/rtwo-vendor.mk', 'vendor/motorola/sm8550-common/sm8550-common-vendor.mk']:
    if os.path.isfile(mk):
        L = open(mk).read().split('\n')
        out = [l for l in L if name not in l]
        if len(out) != len(L):
            open(mk, 'w').write('\n'.join(out))
            print('quitado de', mk)
