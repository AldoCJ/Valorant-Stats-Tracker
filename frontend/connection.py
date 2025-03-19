import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Get database credentials from .env file
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "valorant_stats")

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print("Database connection successful!")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None