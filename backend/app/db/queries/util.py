def remove_secure(x: dict):
    print(x)
    x.pop("_secure_", None)
    return x
