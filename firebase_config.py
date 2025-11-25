import os
import json
import firebase_admin
from firebase_admin import credentials, db

if os.path.exists("serviceAccountKey.json"):
    cred = credentials.Certificate("serviceAccountKey.json")

else:
    service_account_info = json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"])
    cred = credentials.Certificate(service_account_info)

firebase_admin.initialize_app(cred, {
    "databaseURL": os.environ["FIREBASE_DB_URL"]
})

def save_user_log(ref_path: str, log_data: dict):
    ref = db.reference(ref_path)
    ref.set(log_data)

def get_db():
    return db