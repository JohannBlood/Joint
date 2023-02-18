from zlib import decompress


f = open('.git/objects/eb/ef51cffdfe0a529c259c0ae6c40338af2f892c', 'rb')
data = f.read()
print(decompress(data).decode())


