import redis
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def set_short_term(user_id, message):
    key = f"stm:{user_id}"
    r.setex(key, 5 *60, json.dumps(message))  # Set with expiration of 5 min

def get_short_term(user_id):
    key = f"stm:{user_id}"
    value = r.get(key)
    return json.loads(value) if value else None

def set_long_term(user_id, fact_id, message):
    key = f"ltm:{user_id}:{fact_id}"
    r.hset(key, mapping={"fact": message})

def get_long_term(user_id):
    keys = r.keys(f"ltm:{user_id}:*")
    result = []
    for key in keys:
        fact = r.hget(key, "fact")
        result.append(fact)
    return result


# ---------- TEST IT ----------
if __name__ == "__main__":
    print("🔁 Testing short-term memory...")
    chat = [
        {"role": "user", "message": "Hello"},
        {"role": "assistant", "message": "Hi! How can I help you today?"}
    ]
    set_short_term("user123", chat)
    print("STM:", get_short_term("user123"))

    print("\n🧠 Testing long-term memory...")
    set_long_term("user123", "1", "User likes natural language processing.")
    set_long_term("user123", "2", "User asked about Redis memory.")
    print("LTM:", get_long_term("user123"))