import os
from dotenv import load_dotenv
from censys_platform import SDK

load_dotenv() 

sdk = SDK(
    personal_access_token=os.getenv("CENSYS_API_KEY"),
)

def censys():
    pass