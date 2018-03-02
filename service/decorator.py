import os
import base64
import functools
from aiohttp.web import Response

ADMIN = os.getenv("ADMIN")
PWD = os.getenv("ADMINPWD")

def require_admin_login(f):
    @functools.wraps(f)
    async def decorator(request, *args, **kwargs):
        authorized = False
        headers = request.headers
        req_headers = dict(headers)

        basic_auth_header = req_headers.get('Authorization')
        if basic_auth_header:
            auth_header = basic_auth_header[6:]
            admin, pwd = base64.b64decode(auth_header).decode().split(':')
            if admin == ADMIN and \
               pwd == PWD :
                   authorized = True
            else: return Response(body = b'{}',
                content_type = 'application/json', status = 403)

        if authorized:
            response = await f(request)
            return response
        else:
            return Response(body = b'{}',
            content_type = 'application/json', status = 401)
    return decorator