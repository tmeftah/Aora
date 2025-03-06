import os
import sys

from fastapi.testclient import TestClient

from backend.main import app

sys.path.append(os.getcwd())


client = TestClient(app)
