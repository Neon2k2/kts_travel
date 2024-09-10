from firebase_admin import firestore
from google.cloud import exceptions
import hashlib

db = firestore.client()


def add_admin(username, password, role):
    hashed_password = hash_password(password)
    admin_ref = db.collection('admins').add({
        'username': username,
        'password': hashed_password,
        'role': role
    })
    return admin_ref.id

def hash_password(password):
    # Hash password using SHA-256
    return hashlib.sha256(password.encode()).hexdigest()

def add_log(log_data):
    try:
        db.collection('logs').add(log_data)
    except exceptions.GoogleCloudError as e:
        raise Exception(f"Firestore error: {str(e)}")

def get_logs():
    try:
        logs = db.collection('logs').stream()
        return [log.to_dict() for log in logs]
    except exceptions.GoogleCloudError as e:
        raise Exception(f"Firestore error: {str(e)}")

def get_log_by_id(log_id):
    try:
        log = db.collection('logs').document(log_id).get()
        if log.exists:
            return log.to_dict()
        else:
            raise Exception("Log not found")
    except exceptions.GoogleCloudError as e:
        raise Exception(f"Firestore error: {str(e)}")

def update_log(log_id, log_data):
    try:
        log_ref = db.collection('logs').document(log_id)
        if log_ref.get().exists:
            log_ref.update(log_data)
        else:
            raise Exception("Log not found")
    except exceptions.GoogleCloudError as e:
        raise Exception(f"Firestore error: {str(e)}")

def delete_log(log_id):
    try:
        log_ref = db.collection('logs').document(log_id)
        if log_ref.get().exists:
            log_ref.delete()
        else:
            raise Exception("Log not found")
    except exceptions.GoogleCloudError as e:
        raise Exception(f"Firestore error: {str(e)}")

def get_logs_by_driver(driver_id):
    try:
        logs = db.collection('logs').where('driver', '==', driver_id).stream()
        return [log.to_dict() for log in logs]
    except exceptions.GoogleCloudError as e:
        raise Exception(f"Firestore error: {str(e)}")

def get_logs_by_car(car_id):
    try:
        logs = db.collection('logs').where('car', '==', car_id).stream()
        return [log.to_dict() for log in logs]
    except exceptions.GoogleCloudError as e:
        raise Exception(f"Firestore error: {str(e)}")

def get_logs_by_date(date):
    try:
        logs = db.collection('logs').where('date', '==', date).stream()
        return [log.to_dict() for log in logs]
    except exceptions.GoogleCloudError as e:
        raise Exception(f"Firestore error: {str(e)}")
