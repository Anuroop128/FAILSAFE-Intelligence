import os
import sys

# Ensure the root directory is in sys.path so 'app' can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api import app

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
