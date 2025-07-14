from src.models.user import User, db

class UserManager:
    @staticmethod
    def create_default_users():
        """Create default users if they don't exist"""
        default_users = [
            {'username': 'admin', 'password': 'admin123'},
            {'username': 'user1', 'password': 'user123'},
            {'username': 'user2', 'password': 'user123'},
            {'username': 'user3', 'password': 'user123'},
            {'username': 'user4', 'password': 'user123'},
            {'username': 'user5', 'password': 'user123'},
            {'username': 'user6', 'password': 'user123'},
            {'username': 'user7', 'password': 'user123'},
            {'username': 'user8', 'password': 'user123'},
            {'username': 'user9', 'password': 'user123'},
            {'username': 'user10', 'password': 'user123'},
        ]
        
        created_users = []
        
        for user_data in default_users:
            existing_user = User.query.filter_by(username=user_data['username']).first()
            if not existing_user:
                new_user = User(username=user_data['username'])
                new_user.set_password(user_data['password'])
                db.session.add(new_user)
                created_users.append(user_data['username'])
        
        try:
            db.session.commit()
            return created_users
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_user_count():
        """Get total number of users"""
        return User.query.count()
    
    @staticmethod
    def get_active_users():
        """Get all active users"""
        return User.query.filter_by(active=True).all()
    
    @staticmethod
    def deactivate_user(user_id):
        """Deactivate a user"""
        user = User.query.get(user_id)
        if user:
            user.active = False
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def activate_user(user_id):
        """Activate a user"""
        user = User.query.get(user_id)
        if user:
            user.active = True
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def change_password(user_id, new_password):
        """Change user password"""
        user = User.query.get(user_id)
        if user:
            user.set_password(new_password)
            db.session.commit()
            return True
        return False

