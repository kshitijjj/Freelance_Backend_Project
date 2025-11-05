from flask import Flask,request,jsonify,Blueprint
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from Models.Jobs import Jobs
from Models.Users import Users
from config import db
from Models.saved_jobs import Saved_Jobs
from Models.applied_jobs import Applied_Jobs
from datetime import datetime

admin_bp=Blueprint("admin",__name__)

# ADMIN GET ROUTE TO LIST ALL THE JOBS
@admin_bp.route("/admin/jobs",methods=['GET'])
@jwt_required()
def all_jobs():
    jobs=Jobs.query.all()
    all_jobs=[]

    for select_jobs in jobs:
        all_jobs.append({
            "id":select_jobs.id,
            "user_id":select_jobs.user_id,
            "category":select_jobs.category,
            "description":select_jobs.description,
            "salary":select_jobs.salary,
            "created_at":select_jobs.created_at
        })
    return jsonify({"result":all_jobs})

# ADMIN POST ROUTE TO POST THE JOBS
@admin_bp.route("/admin/jobs",methods=['POST'])
@jwt_required()
def job_post():
    data=request.get_json()
    job_category=data['category']
    job_description=data['description']
    salary=data['salary']

    user_id=get_jwt_identity()
    new_job=Jobs(user_id=user_id,category=job_category,description=job_description,salary=salary)
    db.session.add(new_job)
    db.session.commit()

    return jsonify({"message":"Job posted successfully"})

