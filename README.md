# Agent 2 - Web2 Identity & DeFi Reputation Aggregator

Agent 2 is a high-performance FastAPI microservice designed to aggregate Web2 social data and Web3 activity into a unified reputation score for DeFi credit scoring systems.

## 🚀 Features

-   **GitHub Integration**: Fetches public profile data, calculates account age, and extracts repository/follower metrics.
-   **StackOverflow Integration**: Retrieves user reputation and badge counts via the StackExchange API.
-   **Web3 Human Verification (Helius)**: Checks Solana wallet balances and NFT ownership using Helius RPC to confirm "Web3 Human" status.
-   **Social Media Mocking**: Returns placeholder data for LinkedIn to ensure demo stability without scraping risks.
-   **Async Performance**: Uses `httpx` and `asyncio` to perform all external API checks concurrently.
-   **Docker Ready**: Includes a production-optimized Dockerfile for easy deployment.

## 🛠 Tech Stack

-   **Language**: Python 3.11+
-   **Framework**: FastAPI
-   **Asynchronous I/O**: `httpx`, `asyncio`
-   **Server**: Uvicorn
-   **Deployment**: Docker

## 🚦 Getting Started

### Local Development

1.  **Clone the repository**:
    ```bash
    git clone git@github.com:BALAJI-SK/agent-2.git
    cd agent-2
    ```

2.  **Setup Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Run the Server**:
    ```bash
    # Set your Helius API Key (Optional, has fallback)
    export HELIUS_API_KEY="your_helius_key"
    python main.py
    ```

4.  **Test the Endpoint**:
    ```bash
    python test_request.py
    ```

### Running with Docker

```bash
docker build -t agent-2 .
docker run -p 8001:8001 -e HELIUS_API_KEY="your_key" agent-2
```

## 📡 API Reference

### POST `/api/v1/web2-reputation`

**Request Body:**
```json
{
  "github_username": "octocat",
  "stackoverflow_id": "1",
  "solana_address": "nBL2wqYFWcUF67zVP568PAR5BR7X2gjVzbBE13ov2er"
}
```

**Sample Response:**
```json
{
  "status": "success",
  "data": {
    "github": {
      "username": "octocat",
      "account_age_years": 15.0,
      "public_repos": 8,
      "followers": 21876
    },
    "stackoverflow": {
      "user_id": "1",
      "reputation": 64169,
      "badge_counts": {
        "bronze": 153,
        "silver": 153,
        "gold": 48
      }
    },
    "solana": {
      "is_web3_verified": true,
      "sol_balance": 1.25,
      "nft_count": 5,
      "trust_signal": "Verified Web3 Human"
    },
    "social_media": {
      "linkedin_verified": true,
      "connections": "500+"
    }
  },
  "timestamp": "2026-02-21T22:51:43.032583+00:00"
}
```

## ⚖️ License
MIT
