def getJson():
    try:
        from simplejson import json
        jsonModule = json
    except:
        import json
        jsonModule = json
    return jsonModule

def sha256sum(hash,filepath):
    from hashlib import sha256 #hashlib to make our lives easier, no reason to import the whole thing

    with open(filepath, 'r') as f:
        filehash = sha256(f.read()).hexdigest()

    if filehash != hash: return False
    return True