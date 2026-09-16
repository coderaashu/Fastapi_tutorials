from fastapi import FastAPI,Request
import time
app = FastAPI()

@app.middleware("http")
async def log_request(request: Request, call_next):
    print("Request Received")
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    print(f"Response Sent in {process_time} seconds")

    return response


# @app.middleware("http")
# async def log_request(request: Request, call_next):
#     print("Request Received")

#     response = await call_next(request)
#     print("Response Sent")

#     return response