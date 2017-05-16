import hashlib

h = hashlib.md5()

hashlib.md5('22')
print(h.digest)

h.update("22222")
print(h.digest)

h.update("22221")
print(h.digest)
