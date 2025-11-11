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
            "id":jobs.job_id,
            "user_id":user_id,
            "company":jobs.company,
            "work_type":jobs.work_type,
            "job description":jobs.job_description,
            "skills":jobs.skills,
            "experience":jobs.experience,
            "qualifications":jobs.qualifications,
            "salary range":jobs.salary_range,
            "location":jobs.location,
            "company size":jobs.company_size,
            "job posted at":jobs.job_posted_at
        })

    if len(all_jobs)==0:
        return jsonify({"message":"No jobs to show !!"}),400

    return jsonify(all_jobs)

# POST REQUEST TO POST THE JOB
@user_bp.route("/jobs",methods=['POST'])
@jwt_required()
def post_job():
    data=request.get_json()
    job_id=data['job_id']
    company = data['company']
    work_type = data['work_type']
    job_title = data['job_title']
    job_description = data['job_description']        
    skills = data['skills']
    experience = data['experience']
    qualifications = data['qualifications']
    salary_range = data['salary_range']                
    location = data['location']
    country=data['country']
    company_size = data['company_size']
    job_posted_at = data['job_posted_at']

    user_id=get_jwt_identity()

    new_job=Jobs(
        job_id=job_id,
        user_id=user_id,
        company=company,
        work_type=work_type,
        job_title=job_title,
        job_description=job_description,
        skills=skills,
        experience=experience,
        qualifications=qualifications,
        salary_range=salary_range,
        location=location,
        country=country,
        company_size=company_size,
        job_posted_at=job_posted_at
    )
    db.session.add(new_job)
    db.session.commit()

    return jsonify({"message":"Job posted successfully"})

# GET REQUEST TO SAVE THE JOB
@user_bp.route("/jobs/save/<int:id>",methods=['GET'])
@jwt_required()
def saved_job(id):
    user_id=get_jwt_identity()
    
    is_job=Saved_Jobs.query.filter(Saved_Jobs.job_id==id).first()

    if not is_job:
        
        saved_job=Saved_Jobs(user_id=user_id,job_id=id,saved_at=datetime.utcnow())
        db.session.add(saved_job)
        db.session.commit()
        return jsonify({"message":"JOb saved"})
    else:
        return jsonify({"message":"job already added"})

    

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
    user_id=get_jwt_identity()
    job_title=request.args.get("job_title")
    salary_range=request.args.get("salary_range")
    company=request.args.get("company")
    location=request.args.get("location")
    job_posted_at=request.args.get("job_posted_at")

    query=Jobs.query

    if job_title:
        query=query.filter(Jobs.job_title==job_title)
    if salary_range:
        query=query.filter(Jobs.salary_range<=salary_range)
    if job_posted_at:
        correct_date=datetime.strptime(job_posted_at,"%Y-%m-%d")
        query=query.filter(Jobs.created_at<=correct_date)
    if company:
        query=query.filter(Jobs.company==company)
    if location:
        query=query.filter(Jobs.location==location)

    selected_jobs=query.all()
    searched_jobs=[]

    for jobs in selected_jobs:
        searched_jobs.append({
            "id":jobs.job_id,
            "user_id":jobs.user_id,
            "company":jobs.company,
            "work_type":jobs.work_type,
            "job description":jobs.job_description,
            "skills":jobs.skills,
            "experience":jobs.experience,
            "qualifications":jobs.qualifications,
            "salary range":jobs.salary_range,
            "location":jobs.location,
            "company size":jobs.company_size,
            "job posted at":jobs.job_posted_at
        })
    
    return jsonify({"result":searched_jobs})