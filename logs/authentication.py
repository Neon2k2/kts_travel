# logs/authentication.py
import hashlib
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from firebase_admin import firestore
from google.cloud import exceptions

db = firestore.client()

def hash_password(password):
    # Hash password using SHA-256
    return hashlib.sha256(password.encode()).hexdigest()

class FirestoreBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Query Firestore for the admin user
            admin_ref = db.collection('admins').where('username', '==', username).limit(1).get()
            if not admin_ref:
                return None

            admin_data = admin_ref[0].to_dict()
            if admin_data.get('password') == hash_password(password):  # Check hashed password
                # Create or get the Django user
                user, created = User.objects.get_or_create(username=username)
                return user
            return None
        except exceptions.GoogleCloudError as e:
            raise Exception(f"Firestore error: {str(e)}")

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
