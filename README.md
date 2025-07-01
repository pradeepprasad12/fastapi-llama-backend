# 🧠 FastAPI + Replicate LLaMA-4 Prompt API

A FastAPI-based backend that takes user prompts, sends them to Replicate's LLaMA-4 model, stores the prompt/response history, and returns the result.

---

## 📦 Setup Instructions

```bash
# Clone the repo
git clone https://github.com/pradeepprasad12/fastapi-llama-backend.git
cd fastapi-llama-backend

# Create a virtual environment
python -m venv env
source env/bin/activate  # or `env\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt
#for run
uvicorn app.main:app --reload 


#api
Step 1: Login and get a token
- POST
-http://localhost:8000/login/
- {"username": "alice", "password": "secret1"}
-Response- 
{
  "token": "token_alice"
}
Step 2: Send a prompt to the LLaMA model
- post
- http://localhost:8000/prompt/
-"Authorization: Bearer token_alice" 
  -H "Content-Type: application/json" 
  -d '{"prompt": "What is FastAPI and why is it useful?"}'

Response-
{
  "response": "FastAPI is a modern Python web framework for building APIs quickly..."
}

Step 3: Get your prompt history
- GET 
- http://localhost:8000/history/

Response-
{
  "history": [
    {
      "timestamp": "2025-06-28T12:34:56Z",
      "prompt": "What is FastAPI and why is it useful?",
      "response": "FastAPI is a modern Python web framework..."
    }
  ]
}

##
Create a .env file and  create a variable "REPLICATE_API_TOKEN" put your api key 


####### Application Architecture Diagram  ##########3333333

Client (Thunder Client / Frontend / Postman)
    |
    v
[FastAPI App: /prompt endpoint]
    |
    v
[auth_user Dependency]
    |
    v
[run_llama(prompt) - replicate_service.py]
    |
    v
Create a prediction -> Replicate API
    |
    v
Poll status URL until complete -> Replicate API
    |
    v
Get `output` from completed job
    |
    v
Return `response` (text) to route handler
    |
    v
[storage.py -> add(user, prompt, response)]
    |
    v
Save history in memory 
    |
    v
Send final response JSON back to client


##############  Key Components
auth_user → Validates the user (simulated or real auth).

run_llama(prompt) → Sends prompt to Replicate model, waits for result.

storage.add() → Stores prompt-response pair for history retrieval.

Prompt endpoint → Orchestrates everything and returns structured output.