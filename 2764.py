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

async def fetch_numbers_from_server(numberid: str):
    try:
        response = requests.get(f"{THIRD_PARTY_URL}/{numberid}", timeout=0.5)
        response.raise_for_status()
        return response.json().get('numbers', [])
    except (requests.Timeout, requests.RequestException):
        return []

def update_numbers_window(new_numbers):
    global numbers_window
    for number in new_numbers:
        if number not in numbers_window:
            if len(numbers_window) >= window_size:
                numbers_window.pop(0)
            numbers_window.append(number)

def calculate_average():
    if not numbers_window:
        return 0.0
    return round(sum(numbers_window) / len(numbers_window), 2)
