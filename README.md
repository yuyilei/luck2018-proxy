# luck2018-proxy

> 小幸运，每隔一分钟获取一个新的代理。。

*** 

## 环境变量 

**proxyip.env** : 

```
REDIS_HOST=                   //redis host
REDIS_PORT=                   //redis端口
ADMIN=                        // 管理员身份验证
ADMINPWD=                     // 管理员身份验证
CELERY_BROKER_URL=            // celery broker 
API_URL=                      // 获取proxy的api 
```

*** 

## 部署测试 :
```
docker-compose build && docker-compose up & 
```

***


## api文档 : 

**获取IP**

|URL|Header|Method|
|---| -- | -- |
|/api/ip/| 管理员headers| GET |

**URL Params:None** 

**POST Data: None**

**RETURN Data:** 
```
{
    "IP": "115.203.185.176",
    "port": "32813"
}
```

**Status Code :**
```
200 // 成功
403或401 // 管理员身份验证错误
```

