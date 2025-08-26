import mysql.connector
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()

# Get database credentials from .env file
DB_HOST = os.getenv("HOST", "metro.proxy.rlwy.net")
DB_USER = os.getenv("USER", "root")
DB_PASSWORD = os.getenv("PASSWORD", "")
DB_NAME = os.getenv("NAME", "railway")
DB_PORT = os.getenv("PORT", "45442")

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        print("Database connection successful!")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None