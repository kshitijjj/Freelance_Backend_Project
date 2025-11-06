from flask import Flask,request,jsonify,Blueprint
from Models.Users import Users
from Models.Jobs import Jobs
from Models.applied_jobs import Applied_Jobs
from Models.saved_jobs import Saved_Jobs
from flask_jwt_extended import jwt_required,get_jwt,get_jwt_identity
from config import Admin_password,db
from Utils.decorator import admin_required

admin_bp=Blueprint("admin",__name__)

def default_admin():
    admin=Users.query.filter(Users.email=="mayank_admin@gmail.com").first()
    if not admin:
        new_admin=Users(username="Mayank",email="mayank_admin@gmail.com",role="admin")
        new_admin.generate_passwrod(Admin_password)
        db.session.add(new_admin)
        db.session.commit()

# GET ROUTE TO GET ALL THE JOBS LISTED
@admin_bp.route("/admin/jobs",methods=['GET'])
@jwt_required()
@admin_required
def all_jobs():
    user_id=get_jwt_identity()
    required_jobs=Jobs.query.all()

    if not required_jobs:
        return jsonify({"message":"Currently no jobs are posted !"})
    
    selected_jobs=[]
    
    for jobs in required_jobs:
        selected_jobs.append({
            "id":jobs.id,
            "category":jobs.category,
            "description":jobs.description,
            "salary":jobs.salary,
            "created_at":jobs.created_at
        })
    return jsonify({"result":selected_jobs})


## POST ROUTE TO POST THE JOBS
@admin_bp.route("/admin/jobs",methods=['POST'])
@jwt_required()
@admin_required
def post_jobs():
    data=request.get_json()

    user_id=get_jwt_identity()

    for jobs in data:
        new_job=Jobs(
            user_id=user_id,
            category=jobs['category'],
            description=jobs['description'],
            salary=jobs['salary']
        )
        db.session.add(new_job)
    db.session.commit()

    return jsonify({"message":"All jobs posted successfully"})

# GET ROUTE TO GET THE TOTAL COUNT AND LIST OF USERS LOGIN 
@admin_bp.route("/admin/users",methods=['GET'])
@jwt_required()
@admin_required
def all_users():
    user_id=get_jwt_identity()
    required_users=Users.query.filter(Users.role!="admin").all()

    users_list=[]

    for users in required_users:
        users_list.append({
            "user_id":user_id,
            "username":users.username
        })
    
    return jsonify({"total users":len(users_list),"User_Details":users_list})