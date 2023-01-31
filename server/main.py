import uvicorn

from database import Database
from server import app

if __name__ == "__main__":
    db = Database() # Initialize the database
    uvicorn.run(app, host="0.0.0.0", port=80)  # Run FastAPI
