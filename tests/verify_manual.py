import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ /health check passed!")
            print(response.json())
        else:
            print(f"❌ /health check failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Connection failed: {e}")

def test_chat():
    print("\nTesting /chat endpoint (expecting 401/403 without token)...")
    url = f"{BASE_URL}/chat"
    payload = {
        "message": "Hello Zenith, are you online?",
        "session_id": "test-session-1"
    }
    try:
        # Note: This is expected to fail auth if we don't provide a token, 
        # but it confirms the endpoint is reachable.
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 401 or response.status_code == 403:
             print("✅ Endpoint reachable (Auth enforced)")
        elif response.status_code == 200:
             print("✅ Endpoint success!")
             for line in response.iter_lines():
                 if line:
                     print(line.decode('utf-8'))
        else:
             print(f"❌ Unexpected status: {response.status_code}")
             print(response.text)

    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    test_health()
    test_chat()
