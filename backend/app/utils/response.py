def ok(data=None):
    return {"success": True, "data": data}

def err(msg, code=400):
    return {"success": False, "error": msg, "code": code}
