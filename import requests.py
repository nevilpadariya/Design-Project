import requests

url = "https://tns4lpgmziiypnxxzels5s5nyu0nftol.lambda-url.us-east-1.on.aws/ramp-challenge-instructions/"

# Send a POST request to the URL
response = requests.post(url)

# Print the JSON response from the server
print(response.json())