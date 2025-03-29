#!/bin/bash

# Test the /safetyCheck endpoint using curl
echo "Testing /safetyCheck endpoint with curl..."

# URL for the endpoint
URL="http://127.0.0.1:5001/ai-hackathon-202503/us-central1/api/safetyCheck"

echo "Making GET request to: $URL"
curl -v "$URL"

echo -e "\n\nDone!"
