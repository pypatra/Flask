from app import db, bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    def setPassword(self, password: str) -> None:
        self.password = bcrypt.generate_password_hash(password)
        
    def checkPassword(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return '<User {}>'.format(self.username)