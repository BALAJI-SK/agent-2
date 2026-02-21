from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import httpx
import asyncio
import os
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

app = FastAPI(title="Agent 2 - Web2 Identity Aggregator")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ReputationRequest(BaseModel):
    github_username: Optional[str] = None
    stackoverflow_id: Optional[str] = None
    solana_address: Optional[str] = None

async def get_github_data(username: str) -> Optional[Dict[str, Any]]:
    if not username:
        return None
    
    url = f"https://api.github.com/users/{username}"
    headers = {"User-Agent": "Agent2-Microservice"}
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                created_at = datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                now = datetime.now(timezone.utc).replace(tzinfo=None) # Keep it naive for relativedelta comparison if needed, or update comparison logic
                
                # Calculate age in years
                age_delta = relativedelta(now, created_at)
                account_age_years = age_delta.years + (age_delta.months / 12.0)
                
                return {
                    "username": username,
                    "account_age_years": round(account_age_years, 2),
                    "public_repos": data.get("public_repos"),
                    "followers": data.get("followers")
                }
            return None
    except Exception as e:
        print(f"GitHub API Error: {e}")
        return None

async def get_stackoverflow_data(user_id: str) -> Optional[Dict[str, Any]]:
    if not user_id:
        return None
    
    url = f"https://api.stackexchange.com/2.3/users/{user_id}?site=stackoverflow"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            if response.status_code == 200:
                items = response.json().get("items", [])
                if items:
                    user = items[0]
                    return {
                        "user_id": user_id,
                        "reputation": user.get("reputation"),
                        "badge_counts": user.get("badge_counts")
                    }
            return None
    except Exception as e:
        print(f"StackOverflow API Error: {e}")
        return None
async def check_helius_reputation(wallet_address: str) -> Dict[str, Any]:
    if not wallet_address:
        return {"is_web3_verified": False, "sol_balance": 0, "nft_count": 0}
        
    # Retrieve Helius API key from environment variable
    api_key = os.getenv("HELIUS_API_KEY", "35c6b453-6a5c-4a3a-9694-87893116d997") 
    url = f"https://mainnet.helius-rpc.com/?api-key={api_key}"
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # 1. Check SOL Balance
            balance_payload = {
                "jsonrpc": "2.0",
                "id": "1",
                "method": "getBalance",
                "params": [wallet_address]
            }
            
            # 2. Check Assets (NFTs)
            assets_payload = {
                "jsonrpc": "2.0",
                "id": "2",
                "method": "getAssetsByOwner",
                "params": {
                    "ownerAddress": wallet_address,
                    "page": 1,
                    "limit": 10,
                    "displayOptions": {"showFungible": False}
                }
            }
            
            # Execute both calls
            balance_resp, assets_resp = await asyncio.gather(
                client.post(url, json=balance_payload),
                client.post(url, json=assets_payload)
            )
            
            sol_balance = 0
            nft_count = 0
            
            if balance_resp.status_code == 200:
                sol_balance = balance_resp.json().get("result", {}).get("value", 0) / 10**9 # Convert Lamports to SOL
                
            if assets_resp.status_code == 200:
                nft_count = assets_resp.json().get("result", {}).get("total", 0)
                
            # Verification Rule: Must have SOL AND NFTs
            is_verified = sol_balance > 0 and nft_count > 0
            
            return {
                "is_web3_verified": is_verified,
                "sol_balance": round(sol_balance, 4),
                "nft_count": nft_count,
                "trust_signal": "Verified Web3 Human" if is_verified else "Low Web3 Activity"
            }
            
    except Exception as e:
        print(f"Helius API Error: {e}")
        return {"is_web3_verified": False, "error": str(e)}


@app.post("/api/v1/web2-reputation")
async def aggregate_reputation(request: ReputationRequest):
    # Fetch data concurrently
    github_task = get_github_data(request.github_username)
    stackoverflow_task = get_stackoverflow_data(request.stackoverflow_id)
    solana_task = check_helius_reputation(request.solana_address)
    
    github_res, stackoverflow_res, solana_res = await asyncio.gather(
        github_task, stackoverflow_task, solana_task
    )
    
    # Mocked Social Media Data as per Rule 3
    social_media_mock = {
        "linkedin_verified": True,
        "connections": "500+"
    }
    
    return {
        "status": "success",
        "data": {
            "github": github_res,
            "stackoverflow": stackoverflow_res,
            "solana": solana_res,
            "social_media": social_media_mock
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
