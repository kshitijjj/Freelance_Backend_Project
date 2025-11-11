from config import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class Users(db.Model):
    user_id=db.Column(db.BigInteger,primary_key=True)
    username=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(200),nullable=False,unique=True)
    password=db.Column(db.String,nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    job_saved=db.Column(db.BigInteger,db.ForeignKey("jobs.id"))
    job_applied=db.Column(db.BigInteger,db.ForeignKey("jobs.id"))
    role=db.Column(db.String,default="user")

    def generate_passwrod(self,password):
        self.password=generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)
    
