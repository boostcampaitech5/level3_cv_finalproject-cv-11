from fastapi import Depends, APIRouter, HTTPException
from backend.routers import crud
from backend.routers.database import SessionLocal
from deepfake import make_synthesis
from sqlalchemy.orm import Session
import os
import httpx

vertex_router = APIRouter()
# predict_custom_trained_model_sample(
#     project="521316103453",
#     endpoint_id="6332478890501472256",
#     location="us-central1",
#     instances={ "instance_key_1": "value", ...}
# )

# Replace with your actual Google Cloud Project ID and Endpoint ID
PROJECT_ID = "521316103453"
ENDPOINT_ID = "6332478890501472256"

# Replace with the Google Cloud authentication token
# For simplicity, you can set the token directly here, but it's better to handle it securely in production.
# AUTH_TOKEN = "your-google-cloud-auth-token"

'''
{"instances": [
  {"values": [1, 2, 3, 4], "key": 1},
  {"values": [5, 6, 7, 8], "key": 2}
]}
'''
# Endpoint to make predictions
@vertex_router.post("/predict/")
async def predict(input_data: dict):
    try:
        # Define the API endpoint URL
        api_url = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/us-central1/endpoints/{ENDPOINT_ID}:predict"

        # Set the headers for the request
        headers = {
            # "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json"
        }

        # Send the request to Google Cloud Vertex AI endpoint
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, headers=headers, json=input_data)
            response_data = response.json()

        # Check if the response contains the predictions
        if "predictions" in response_data:
            return response_data["predictions"]
        else:
            raise HTTPException(status_code=500, detail="Failed to get predictions from the model")

    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail="Failed to make a request to Google Cloud Vertex AI")
