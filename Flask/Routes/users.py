from flask import Flask,request,jsonify,Blueprint
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from Models.Jobs import Jobs
from Models.Users import Users
from config import db
from Models.saved_jobs import Saved_Jobs
from Models.applied_jobs import Applied_Jobs
from datetime import datetime

user_bp=Blueprint("user",__name__)

# GET REQUEST TO SHOW ALL THE JOBS TO USERS
@user_bp.route("/jobs",methods=['GET'])
@jwt_required()
def all_jobs():
    all_jobs=[]
    user_id=get_jwt_identity()  

    required_jobs=Jobs.query.filter(Jobs.user_id!=user_id).all()

    for jobs in required_jobs:
        all_jobs.append({
            "id":jobs.id,
            "user_id":user_id,
            "category":jobs.category,
            "description":jobs.description,
            "salary":jobs.salary,
            "created_at":jobs.created_at
        })

    if len(all_jobs)==0:
        return jsonify({"message":"No jobs to show !!"}),400

    return jsonify(all_jobs)

# POST REQUEST TO POST THE JOB
@user_bp.route("/jobs",methods=['POST'])
@jwt_required()
def post_job():
    data=request.get_json()
    job_category=data['category']
    job_description=data['description']
    salary=data['salary']

    user_id=get_jwt_identity()
    new_job=Jobs(user_id=user_id,category=job_category,description=job_description,salary=salary)
    db.session.add(new_job)
    db.session.commit()

    return jsonify({"message":"Job posted successfully"})

# GET REQUEST TO SAVE THE JOB
@user_bp.route("/jobs/save/<int:id>",methods=['GET'])
@jwt_required()
def saved_job(id):
    user_id=get_jwt_identity()
    
    is_job=Saved_Jobs.query.filter(Saved_Jobs.job_id==id).first()

    if is_job:
        return jsonify({"message":"Job already saved"})
    else:
        saved_job=Saved_Jobs(user_id=user_id,job_id=id,saved_at=datetime.utcnow())


        db.session.add(saved_job)
        db.session.commit()
        return jsonify({"message":"Job Saved successfully"})

# GET REQUEST TO APPLY THE JOB
@user_bp.route("/jobs/apply/<int:id>",methods=['GET'])
@jwt_required()
def applied_job(id):
    user_id=get_jwt_identity()
    
    is_job=Applied_Jobs.query.filter(Applied_Jobs.job_id==id).first()

    if is_job:
        return jsonify({"message":"Job already applied"})
    else:
        applied_job=Applied_Jobs(user_id=user_id,job_id=id,applied_at=datetime.utcnow())


        db.session.add(applied_job)
        db.session.commit()
        return jsonify({"message":"Job Applied successfully"})

# GET REQUEST TO SEARCH JOBS BY CATEGORY TIME AND SALARY
@user_bp.route("/jobs/search",methods=['GET'])
@jwt_required()
def search_jobs():
    category=request.args.get("category")
    salary=request.args.get("salary")
    date=request.args.get("date")

    query=Jobs.query

    if category:
        query=query.filter(Jobs.category==category)
    if salary:
        query=query.filter(Jobs.salary<=salary)
    if date:
        correct_date=datetime.strptime(date,"%Y-%m-%d")
        query=query.filter(Jobs.created_at<=correct_date)
    
    selected_jobs=query.all()
    searched_jobs=[]

    for jobs in selected_jobs:
        searched_jobs.append({
            "id":jobs.id,
            "user_id":jobs.user_id,
            "category":jobs.category,
            "description":jobs.description,
            "salary":jobs.salary,
            "created_at":jobs.created_at
        })
    
    return jsonify({"result":searched_jobs})