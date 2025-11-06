from config import db
from datetime import datetime

class Applied_Jobs(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"))
    job_id=db.Column(db.Integer,db.ForeignKey("jobs.id"))
    applied_at=db.Column(db.DateTime,default=datetime.utcnow)
    status=db.Column(db.String,nullable=False,default="Applied")
    role=db.Column(db.String,default="user")