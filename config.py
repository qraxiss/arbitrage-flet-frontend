from dotenv import load_dotenv
import os

load_dotenv()

FEE = 1000000

API_URI = os.getenv('API_URI')
FLET_PORT = os.getenv('FLET_PORT')