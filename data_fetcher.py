import requests

BASE_URL = "https://api.openf1.org/v1"
SESSION = "latest"  # change to a session_key number for testing

def get_positions():
    r = requests.get(f"{BASE_URL}/position?session_key={SESSION}")
    return r.json()

def get_intervals():
    r = requests.get(f"{BASE_URL}/intervals?session_key={SESSION}")
    return r.json()

def get_laps(driver_number):
    r = requests.get(f"{BASE_URL}/laps?session_key={SESSION}&driver_number={driver_number}")
    return r.json()

def get_weather():
    r = requests.get(f"{BASE_URL}/weather?session_key={SESSION}")
    return r.json()

def get_pit_stops():
    r = requests.get(f"{BASE_URL}/pit?session_key={SESSION}")
    return r.json()

def get_race_control():
    r = requests.get(f"{BASE_URL}/race_control?session_key={SESSION}")
    return r.json()

def get_drivers():
    r = requests.get(f"{BASE_URL}/drivers?session_key={SESSION}")
    return r.json()

def get_latest_positions():
    r = requests.get(f"{BASE_URL}/position?session_key={SESSION}")
    data = r.json()
    
    # Keep only the latest position per driver
    latest = {}
    for entry in data:
        dn = entry['driver_number']
        latest[dn] = entry  # overwrites with most recent
    
    return list(latest.values())

def get_track_outline():
    # Get one driver's full position history = the track shape
    r = requests.get(f"{BASE_URL}/position?session_key={SESSION}&driver_number=1")
    data = r.json()
    x = [d['x'] for d in data if d.get('x')]
    y = [d['y'] for d in data if d.get('y')]
    return x, y