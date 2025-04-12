import os
from dotenv import load_dotenv

# Get the path of the repository
ROOT_PATH = os.getcwd().split("genai-sous-chef")[0] + "genai-sous-chef"



# Load environment variables from .env file
load_dotenv()

# Access the key
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
MODEL_NAME="gemini-2.0-flash"

