from config import db
from datetime import datetime

class Saved_Jobs(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"))
    job_id=db.Column(db.Integer,db.ForeignKey("jobs.id"))
    saved_at=db.Column(db.DateTime,default=datetime.utcnow)