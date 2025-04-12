import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Access the key
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
MODEL_NAME="gemini-2.0-flash"

