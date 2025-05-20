import redis

r = redis.Redis(host="docker.host.internal", port=6379, decode_responses=True, db="Ayomide-free-db")

# Set and Get test
r.set("Ayomide", "testing work")
value = r.get("Ayomide")
print("Value:", value)