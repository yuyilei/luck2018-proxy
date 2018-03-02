from celery import Celery
import requests
import time
import os
import redis

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL") or "redis://localhost:7384/1"
REDIS_HOST = os.getenv("REDIS_HOST") or "localhost"
REDIS_PORT = os.getenv("REDIS_PORT") or "7384"
api_url = os.getenv("API_URL")

app = Celery('periodic_task',broker=CELERY_BROKER_URL)


def get_ip() :
	while True :
		try :
			r = requests.get(api_url,timeout=120)
		except Exception as err_info:
			print(err_info)
			return

		res = r.json()
		if r.status_code == 200 and res["ERRORCODE"] == "0" :
			break
		time.sleep(20)
	res = res["RESULT"]
	#print(res)
	res = {
		"IP" : res[0]['ip'],
		"port" : res[0]['port']
	}
	return res


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
	# Calls update_ip every 60 seconds.
	sender.add_periodic_task(60.0, update_ip, name='update every 60s')

@app.task
def update_ip() :
	IPconfig = get_ip()
	r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT,db=0)
	r.set('IPconfig',IPconfig)
	print(r.get('IPconfig'),str(int(time.time())))


