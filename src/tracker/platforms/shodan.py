import os
from dotenv import load_dotenv
from shodan import Shodan

load_dotenv() 

api = Shodan(os.getenv("SHODAN_API_KEY"))

def shodan():
    pass