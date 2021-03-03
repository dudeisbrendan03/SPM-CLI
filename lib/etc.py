def getJson():
    try:
        from simplejson import json
        jsonModule = json
    except:
        import json
        jsonModule = json
    return jsonModule