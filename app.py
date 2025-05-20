from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from lstm_redis import set_long_term, get_long_term, set_short_term, get_short_term
from typing import List, Dict
import uvicorn

app = FastAPI()

@app.websocket("/ws/chat/{user_id}")
async def chat_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    try:
        while True:
            user_message = await websocket.receive_text()

            stm = get_short_term(user_id)
            if not isinstance(stm, list):
                stm = []

            stm.append({"role": "user", "message": user_message})
            # set_short_term(user_id, stm)

            reply = f"You said: {user_message}"
            stm.append({"role": "assistant", "message": reply})
            
            print(stm)
            # Save STM chat back to Redis
            set_short_term(user_id, stm)

            # Save full conversation back
            await websocket.send_json(stm)

    except WebSocketDisconnect:
        print(f"WebSocket connection closed for user {user_id}")
        # Optionally, you can clear the short-term memory when the connection is closed
        # r.delete(f"stm:{user_id}")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 
