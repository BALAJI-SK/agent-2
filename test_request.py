import httpx
import json
import asyncio

async def test_endpoint():
    url = "http://127.0.0.1:8001/api/v1/web2-reputation"
    payload = {
        "github_username": "octocat",
        "stackoverflow_id": "1",
        "solana_address": "nBL2wqYFWcUF67zVP568PAR5BR7X2gjVzbBE13ov2er"
    }
    
    print(f"Sending request to {url} with payload: {payload}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=20.0)
            if response.status_code == 200:
                print("Success!")
                print(json.dumps(response.json(), indent=2))
            else:
                print(f"Error: {response.status_code}")
                print(response.text)
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_endpoint())
