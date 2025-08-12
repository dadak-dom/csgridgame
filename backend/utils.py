import mysql.connector
import constants

def connect_db():
    """Connects to MySQL database and returns the connection."""
    try:
        conn = mysql.connector.connect(**constants.DB_CONFIG)
        print("✅ Connected to database successfully!")
        return conn
    except mysql.connector.Error as e:
        print(f"❌ Error connecting to database: {e}")
        return None