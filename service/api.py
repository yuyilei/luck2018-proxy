import os
import aioredis
from aiohttp.web import json_response, Application
from .decorator import require_admin_login

api = Application()
REDIS_HOST = os.getenv("REDIS_HOST") or "localhost"
REDIS_PORT = os.getenv("REDIS_PORT") or "7384"

@require_admin_login
async def get_ip(request) :
	redis = await aioredis.create_redis((REDIS_HOST, REDIS_PORT))
	IPconfig = await redis.get('IPconfig') or '{}'
	redis.close()
	await redis.wait_closed()
	return json_response(eval(IPconfig))

api.router.add_route('GET', '/ip/',get_ip, name='get_ip' )