import asyncio, httpx
from decouple import config
from fastapi import HTTPException, status

BASE_URL  = "https://api.replicate.com/v1/models/meta/llama-4-maverick-instruct/predictions"
API_TOKEN = config("REPLICATE_API_TOKEN")           
TIMEOUT   = 100                                    

async def run_llama(prompt: str) -> str:
    """
    1) POST the prompt to Replicate
    2) Grab the polling URL from response
    3) Poll once per second until status == succeeded
    4) Return the concatenated output text
    """
    if not API_TOKEN:
        raise RuntimeError("Set REPLICATE_API_TOKEN env var")

    headers = {
        "Authorization": f"Token {API_TOKEN}",
        "Content-Type":  "application/json",
    }
    payload = {"input": {"prompt": prompt}}

    async with httpx.AsyncClient(timeout=TIMEOUT, headers=headers) as client:
        # --- create prediction ---------------------------------------------
        data = await client.post(BASE_URL, json=payload) # all response store on data variable
        if data.status_code != 201:
            raise HTTPException(status.HTTP_502_BAD_GATEWAY, data.text)

        job = data.json() #convert into json data
        poll_url = job["urls"]["get"] # find get() api url where ans is stored

        # --- poll until finished -------------------------------------------
        while job["status"] not in ("succeeded", "failed", "canceled"):
            await asyncio.sleep(1)          # 1 sec pause avoids spamming
            job = (await client.get(poll_url)).json() # hit this url and get data

    if job["status"] != "succeeded":
        raise HTTPException(502, f"Inference failed: {job.get('error')}")

    # --- return clean text -------------------------------------------------
    return "".join(job["output"]).strip() #all ans in this output variable ,which we return and store in json storage
