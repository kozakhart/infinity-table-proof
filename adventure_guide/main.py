from fastapi import FastAPI, WebSocket, Request
from contextlib import asynccontextmanager
import httpx
from employees_pb2 import Employees
from dotenv import load_dotenv
import os

load_dotenv()

UNITY_URL = os.getenv("UNITY_URL") or "http://localhost:8080/upload-protobuf"
# default just does endless loop back to the same service

API_KEY='abc123'
@asynccontextmanager
async def app_lifespan(app: FastAPI):

    app.requests_client = httpx.AsyncClient(
        timeout=httpx.Timeout(5.0, connect=5.0),
        headers={"Authorization": f"{API_KEY}"}
    )

    yield
    await app.requests_client.aclose()

app = FastAPI(lifespan=app_lifespan)


@app.post("/upload-protobuf")
async def upload_protobuf(request: Request):
    # Read raw binary protobuf data from the request body
    raw_data = await request.body()

    # Deserialize the data into an Employees message
    employees = Employees()
    employees.ParseFromString(raw_data)

    # Log or process the employees as needed
    for emp in employees.employee:
        print(f"Received Employee: ID={emp.id}, Name={emp.name}, Salary={emp.salary}")

    # Serialize the data to send to another endpoint (assuming the other service expects protobuf)
    serialized_data = employees.SerializeToString()

    # Call the other endpoint passing the serialized protobuf data
    response = await send_protobuf_to_other_service(serialized_data)

    # Handle the response as needed
    if response.status_code == 200:
        return {"message": "Data sent successfully", "response": response.json()}
    else:
        return {"message": "Failed to send data", "error": response.text}
    
async def send_protobuf_to_other_service(serialized_data: bytes):
    url = UNITY_URL  # Replace with the actual URL
    headers = {"Content-Type": "application/protobuf"}  # Set the appropriate content type

    # Use httpx to make the HTTP request to the other service
    async with httpx.AsyncClient() as client:
        response = await client.post(url, content=serialized_data, headers=headers)
    
    return response