#!/bin/bash

# Create a new timeline post
echo "Creating a new timeline post..."
url --request POST http://localhost:5000/api/timeline_post -d 'name=Wei&email=wei.he@mlh.io&content=Just Added Database to my portfolio site!'

# Retrieve all timeline posts
echo "Retrieving all timeline posts..."
GET_RESPONSE=$(curl -s http://localhost:5000/api/timeline_post)
curl http://localhost:5000/api/timeline_post

POST_ID=$(echo "$GET_RESPONSE" | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')

if [ -z "$POST_ID" ]; then
  echo "Failed to create a timeline post."
  exit 1
fi

# Delete the test timeline post
echo "Deleting the test timeline post with ID $POST_ID"
DELETE_RESPONSE=$(curl -s -X DELETE $BASE_URL/$POST_ID)

echo "Script completed."
