from fastapi import FastAPI, HTTPException
import requests
import asyncio

app = FastAPI()

# In-memory storage for numbers
numbers_window = []
window_size = 10

# Third-party server URL (replace with the actual URL)
THIRD_PARTY_URL = "https://example.com/numbers"

@app.get("/numbers/{numberid}")
async def get_numbers(numberid: str):
    if numberid not in ['p', 'f', 'e', 'r']:
        raise HTTPException(status_code=400, detail="Invalid number ID")
    
    window_prev_state = numbers_window.copy()
    new_numbers = await fetch_numbers_from_server(numberid)
    
    if new_numbers:
        update_numbers_window(new_numbers)
    
    avg = calculate_average()
    response = {
        "windowPrevState": window_prev_state,
        "windowCurrState": numbers_window,
        "numbers": new_numbers,
        "avg": avg
    }
    
    return response
