import struct, sys, os
img, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
f = open(img, 'rb')
f.seek(4096)
g = f.read(52)
magic, _, _ = struct.unpack('<III', g[:12])
print('geometry magic: %08x (esperado 616c4467)' % magic)
max_size, slots, _ = struct.unpack('<III', g[44:56]) if len(g) >= 56 else (0, 0, 0)
f.seek(4096)
g = f.read(64)
max_size = struct.unpack('<I', g[44:48])[0]
f.seek(12288)
h = f.read(256)
hm, maj, mnr, hsize = struct.unpack('<IHHI', h[:12])
print('header magic: %08x (esperado 414c5030)  v%d.%d hsize=%d' % (hm, maj, mnr, hsize))
tsize = struct.unpack('<I', h[44:48])[0]
p_off, p_n, p_sz, e_off, e_n, e_sz = struct.unpack('<IIIIII', h[80:104])
f.seek(12288 + hsize)
tables = f.read(tsize)
parts = []
for i in range(p_n):
    b = tables[p_off + i * p_sz: p_off + (i + 1) * p_sz]
    name = b[:36].split(b'\0')[0].decode()
    attr, first, num, grp = struct.unpack('<IIII', b[36:52])
    parts.append((name, first, num))
exts = []
for i in range(e_n):
    b = tables[e_off + i * e_sz: e_off + (i + 1) * e_sz]
    ns, tt, td, ts = struct.unpack('<QIQI', b[:24])
    exts.append((ns, tt, td))
for name, first, num in parts:
    if num == 0:
        continue
    size = sum(exts[first + k][0] for k in range(num)) * 512
    if size == 0:
        continue
    path = os.path.join(out, name + '.img')
    with open(path, 'wb') as o:
        for k in range(num):
            ns, tt, td = exts[first + k]
            if tt != 0:
                continue
            f.seek(td * 512)
            left = ns * 512
            while left > 0:
                c = f.read(min(left, 16 << 20))
                o.write(c)
                left -= len(c)
    print('%-28s %8.1f MB' % (name + '.img', size / 1048576))
