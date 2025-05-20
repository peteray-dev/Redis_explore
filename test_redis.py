import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# Set and Get test
r.set("test:key", "Redis from Python")
value = r.get("test:key")
print("Value:", value)