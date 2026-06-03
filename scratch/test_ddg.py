import httpx

url = "https://nominatim.openstreetmap.org/search?q=dentist+Houston+TX&format=json&addressdetails=1&limit=5"
headers = {
    "User-Agent": "DMCAShieldAgency/1.0 (contact@dmcashield.app)"
}

try:
    r = httpx.get(url, headers=headers)
    print("OSM Status Code:", r.status_code)
    print("Response:")
    print(r.json()[:2])
except Exception as e:
    print("Error:", e)
