from zlib import decompress
from glob import iglob
from os.path import basename, dirname


# f = open('.git/objects/eb/ef51cffdfe0a529c259c0ae6c40338af2f892c', 'rb')
# data = f.read()
# print(decompress(data).decode())
for store in iglob('.git/objects/??/*'):
    id = basename(dirname(store)) + basename(store)
    # print(f'{store=}\n{dirname(store)=}\n{basename(store)=}\n{id=}')
    with open(store, 'rb') as f:
        obj = decompress(f.read())
        # print(obj)
        header, _, body = obj.partition(b'\x00')
        # print(header.split(), 'wtf')
        kind, size = header.split()
    print(id, kind.decode())
    if kind == b'tree':
        tail = body
        while tail:
            treeobj, _, tail = tail.partition(b'\x00')
            # print(treeobj, '\n', tail)
            tmode, tname = treeobj.split()
            num, tail = tail[:20], tail[20:]
            print(f'\t{tname.decode()} {tmode.decode()} {num.hex()}')
    elif kind == b'commit':
        out = body.decode().replace('\n', '\n\t')
        print(f'\t{out}')

