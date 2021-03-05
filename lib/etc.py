def getJson():
    try:
        from simplejson import json
        jsonModule = json
    except:
        import json
        jsonModule = json
    return jsonModule

def sha256sum(hash,filename, block_size=65536):
    from hashlib import sha256 #hashlib to make our lives easier, no reason to import the whole thing
    sha256 = sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    if hash == sha256.hexdigest(): return True
    else: return False