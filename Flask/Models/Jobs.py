from config import db
from datetime import datetime

class Jobs(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"))
    category=db.Column(db.String,nullable=False)
    description=db.Column(db.String)
    salary=db.Column(db.Integer,nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)