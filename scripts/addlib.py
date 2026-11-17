import os, re, subprocess, shutil, sys
V = os.path.expanduser('~/aospa/vendor/motorola/sm8550-common')
S = os.path.expanduser('~/stock/vend/lib64')
bpf = V + '/Android.bp'
mkf = V + '/sm8550-common-vendor.mk'
PLAT = {'liblog','libcutils','libutils','libc++','libc','libm','libdl','libion','libbase','libhidlbase','libhardware'}
declared = set(re.findall(r'name: "([^"]+)"', open(bpf).read()))
todo = [l for l in sys.argv[1:] if l not in declared]
nf = [l for l in todo if not os.path.exists(S + '/' + l + '.so')]
if nf:
    print('NO estan en el stock:', nf, '- no se modifico nada')
    raise SystemExit
def deps_of(p):
    o = subprocess.run(['readelf', '-d', p], capture_output=True, text=True).stdout
    return re.findall(r'NEEDED.*\[(.+)\.so\]', o)
tpl = '\ncc_prebuilt_library_shared {\n    name: "%s",\n    owner: "motorola",\n    strip: {\n        none: true,\n    },\n    target: {\n        android_arm64: {\n            srcs: [\n                "proprietary/vendor/lib64/%s.so",\n            ],\n            shared_libs: [\n%s            ],\n        },\n    },\n    compile_multilib: "64",\n    prefer: true,\n    soc_specific: true,\n}\n'
blocks = ''
for l in todo:
    dst = V + '/proprietary/vendor/lib64/' + l + '.so'
    if not os.path.exists(dst):
        shutil.copy(S + '/' + l + '.so', dst)
    deps = deps_of(S + '/' + l + '.so')
    keep = [d for d in deps if d in PLAT or d in declared or d in todo]
    miss = [d for d in deps if d not in keep]
    print(l, '-> dependencias sin modulo:', miss)
    blocks += tpl % (l, l, ''.join('                "%s",\n' % k for k in keep))
if todo:
    open(bpf, 'a').write(blocks)
    lines = open(mkf).read().split('\n')
    out = []
    for x in lines:
        out.append(x)
        if x.strip() == 'libar-pal \\':
            out += ['    ' + l + ' \\' for l in todo]
    open(mkf, 'w').write('\n'.join(out))
print('Listo:', todo)
