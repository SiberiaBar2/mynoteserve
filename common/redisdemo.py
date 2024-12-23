import redis
# 不推荐这样写
# red = redis.Redis(host='0.0.0.0', port=6379, db=1)

# 使用连接池的方式进行连接 这样他就会对我们的连接尽心一个管理
pool = redis.ConnectionPool(
   host='0.0.0.0', port=6379, db=1,
    decode_responses=True # 这个参数如果不加， 下边就给你返回bytes，需要转换才能看到中文
)

redis_client = redis.Redis(connection_pool=pool)

# 字符串类型的处理
redis_client.set("name","牛耕") # 单独设置一个值
print('redis_client',redis_client.get('name')) # 牛耕

# 设置多个值
redis_client.mset({
    "age": 18,
    "address": "hangzhou"
})

# ['牛耕', '18', 'hangzhou'] 返回的是列表
print('redis_client.mget',redis_client.mget('name', "age", "address"))

# 判断key是否存在 存在是1 不存在是0
print(redis_client.exists('name')) # 1
print(redis_client.exists('myname')) # 0

# 也可以用 get 方法进行判断
print(redis_client.get('myname')) # None

#  获取长度
print(redis_client.dbsize()) # 3

# 持久化时间
print(redis_client.lastsave()) # 2024-12-23 12:30:06

#  ========================== 操作hash类型数据  ==========================
# 新增一个数据
redis_client.hset(name="userhash", key='username', value='牛恒')
# 新增多个
redis_client.hset(name="userhash2", mapping={
    'username': '牛恒', "password": '12333',
    "nickname": '牛还', "address":'hangzhou'
})

# 获取
print(redis_client.hget('userhash2', "username"))
print(redis_client.hgetall('userhash2'))

#  ========================== 操作list set类型数据  ==========================

redis_client.rpush("numberRrig", 1,2,3,4)
redis_client.lpush("numberLrig", 1,2,3,4)


for i in range(redis_client.llen('numberRrig')):
    print('--->',redis_client.lindex('numberRrig', i))

redis_client.sadd('setNume', 11, 12,13,14)
set_num = redis_client.smembers('setNume')

for sm in set_num:
    print(sm)

#  ========================== 操作zset类型数据  =========================
redis_client.zadd('muzset', {
    "v1":10,
    "v2":20,
    "v3":30,
    "v4":40
})

r = redis_client.zrangebyscore('muzset', 20, 30)
print(r) # ['v2', 'v3']


r = redis_client.zrangebyscore('muzset', 20, 30, withscores=True)
print(r) # [('v2', 20.0), ('v3', 30.0)]

# 查成员的索引
print(redis_client.zrank('muzset', "v2"))

