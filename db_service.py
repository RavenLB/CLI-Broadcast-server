from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, UserModel, ActiveConnection
import hashlib
import os

class DatabaseService:
    def __init__(self):
        self.engine = create_engine('sqlite:///chat.db', echo=False)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        try:
            hashed_password = self.hash_password(password)
            print(f"DEBUG: Creating new user: {username}")  # Debug print
            user = UserModel(username=username, password=hashed_password)
            self.session.add(user)
            self.session.commit()
            print(f"DEBUG: User {username} created successfully")  # Debug print
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Registration error: {e}")
            return False

    def verify_user(self, username, password):
        try:
            user = self.session.query(UserModel).filter_by(username=username).first()
            if user and user.password == self.hash_password(password):
                return True
            return False
        except Exception as e:
            print(f"Verification error: {e}")
            return False

    def add_active_connection(self, username):
        try:
            user = self.session.query(UserModel).filter_by(username=username).first()
            if user:
                # Remove any existing connection
                self.remove_active_connection(username)
                # Create new connection
                connection = ActiveConnection(user=user)
                self.session.add(connection)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            print(f"Connection error: {e}")
            return False

    def remove_active_connection(self, username):
        try:
            user = self.session.query(UserModel).filter_by(username=username).first()
            if user and user.active_connection:
                self.session.delete(user.active_connection)
                self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Disconnection error: {e}")

    def get_active_users(self):
        try:
            active_users = self.session.query(UserModel).join(ActiveConnection).all()
            return [user.username for user in active_users]
        except Exception as e:
            print(f"Active users query error: {e}")
            return []

    def cleanup(self):
        self.session.close() 