from flask import Flask, jsonify, request
import requests
import time

app = Flask(__name__)
window_size = 10
window = []

# Endpoints for the third-party APIs
API_ENDPOINTS = {
    'p': 'http://20.244.56.144/test/primes',
    'f': 'http://20.244.56.144/test/fibonacci',
    'e': 'http://20.244.56.144/test/even',
    'r': 'http://20.244.56.144/test/random'
}

def fetch_numbers(api_url):
    try:
        start_time = time.time()
        response = requests.get(api_url, timeout=0.5)
        elapsed_time = time.time() - start_time
        if response.status_code == 200 and elapsed_time <= 0.5:
            return response.json().get('numbers', [])
    except requests.RequestException:
        pass
    return []

def update_window(new_numbers):
    global window
    unique_numbers = list(filter(lambda x: x not in window, new_numbers))
    window.extend(unique_numbers)
    if len(window) > window_size:
        window = window[-window_size:]

def calculate_average():
    if len(window) == 0:
        return 0.0
    return sum(window) / len(window)

@app.route('/numbers/<string:number_id>', methods=['GET'])
def get_numbers(number_id):
    if number_id not in API_ENDPOINTS:
        return jsonify({"error": "Invalid number ID"}), 400

    api_url = API_ENDPOINTS[number_id]
    new_numbers = fetch_numbers(api_url)

    window_prev_state = list(window)
    update_window(new_numbers)
    avg = calculate_average()

    response = {
        "windowPrevState": window_prev_state,
        "windowCurrState": window,
        "numbers": new_numbers,
        "avg": round(avg, 2)
    }

    return jsonify(response)

if __name__ == '_main_':
    app.run(debug=True, port=3001) 