from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from lstm_redis import set_long_term, get_long_term, set_short_term, get_short_term
from typing import List, Dict
import uvicorn
import openai
from dotenv import load_dotenv
import os
import uuid

app = FastAPI()

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(chat_history: List[Dict[str, str]]) -> str:
    messages = [{"role": msg["role"], "content": msg["message"]} for msg in chat_history]
    messages = messages[-10:]  # Limit to the last 10 messages

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=150,
    )

    return response.choices[0].message.content

@app.websocket("/ws/chat/{user_id}")
async def chat_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    try:
        while True:

            user_message = await websocket.receive_text()

            if user_message.strip().lower() == "/recall":
                facts = get_long_term(user_id)
                await websocket.send_json([
                    {"role": "memory", "message": f["fact"] if isinstance(f, dict) else f} for f in facts
                ])
                continue

            stm = get_short_term(user_id) or []

            stm.append({"role": "user", "message": user_message})
            # set_short_term(user_id, stm)

            reply = generate_response(stm)
            stm.append({"role": "assistant", "message": reply})
            
            print(stm)
            # Save STM chat back to Redis
            set_short_term(user_id, stm)
            set_long_term(user_id, str(uuid.uuid4()), f"User said: {user_message}")
            set_long_term(user_id, str(uuid.uuid4()), f"Bot replied: {reply}")

            # Save full conversation back
            await websocket.send_json(stm)

    except WebSocketDisconnect:
        print(f"WebSocket connection closed for user {user_id}")
        # Optionally, you can clear the short-term memory when the connection is closed
        # r.delete(f"stm:{user_id}")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 
