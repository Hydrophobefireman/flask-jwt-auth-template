from flask import Request

from app.settings import app_settings


def prod_ip_resolver(req: Request):
    headers = req.headers
    cf = (
        headers.get("Fly-Client-IP")
        or headers.get("x-real-ip")
        or headers.get("cf-connecting-ip")
    )
    if cf:
        return cf
    return headers.get("x-forwarded-for", req.remote_addr or "").split(",")[-1].strip()


def dev_ip_resolver(req: Request):
    host = req.remote_addr
    print("[ip]", host)
    return host


ip_resolver = prod_ip_resolver if app_settings.is_prod else dev_ip_resolver
