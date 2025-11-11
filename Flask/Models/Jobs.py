from config import db
from datetime import datetime

class Jobs(db.Model):
    id=db.Column(db.BigInteger,primary_key=True)
    job_id=db.Column(db.BigInteger,nullable=False)
    user_id=db.Column(db.BigInteger,db.ForeignKey("users.user_id"))
    company=db.Column(db.String,nullable=False)
    work_type=db.Column(db.String,nullable=False)
    job_title=db.Column(db.String,nullable=False)
    job_description=db.Column(db.String)
    skills=db.Column(db.String)
    experience=db.Column(db.String)
    qualifications=db.Column(db.String)
    salary_range=db.Column(db.String,nullable=False)
    location=db.Column(db.String,nullable=False)
    country=db.Column(db.String,nullable=False)
    company_size=db.Column(db.BigInteger,nullable=False)
    job_posted_at=db.Column(db.String,nullable=False)
