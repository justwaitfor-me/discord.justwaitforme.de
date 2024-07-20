import requests
from urllib.parse import urlencode


def main(key):
  # Define the API endpoint URL
  base_url = "http://localhost/justwaitforme/projects/discord.justwaitforme.de/api/"

  # Build the URL with the passcode parameter
  params = {"code": "34095IOFH=E2ß0592/234hf3ß59", "key":key}
  url = f"{base_url}?{urlencode(params)}"

  # Send a GET request to the API
  response = requests.get(url)

  # Check the response status code
  if response.status_code == 200:
    # Access granted! Parse the JSON response (if any)
    data = response.json()
    return data["message"]  
  else:
    # Access denied!
    return False
    
if __name__ == "__main__":
  main()
  
  