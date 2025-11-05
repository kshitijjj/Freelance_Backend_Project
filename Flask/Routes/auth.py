from flask import Flask,request,jsonify,Blueprint
from Models.Users import Users
from config import db
from flask_jwt_extended import create_access_token

auth_bp=Blueprint("auth",__name__)

# SIGNUP - ROUTE
@auth_bp.route("/user/signup",methods=['POST'])
def signup():
    data=request.get_json()
    username=data['username']
    email=data['email']
    password=data['password']

    is_User=Users.query.filter(Users.email==email).first()

    if is_User:
        return jsonify({"messaege":"User already exists! PLease login !!"}),401

    new_User=Users(username=username,email=email)
    new_User.generate_passwrod(password)
    db.session.add(new_User)
    db.session.commit()
    return jsonify({"message":"User Sign up successfully"})

# LOGIN - ROUTE
@auth_bp.route("/user/login",methods=['POST'])
def login():
    data=request.get_json()
    email=data['email']
    password=data['password']
    
    is_User=Users.query.filter(Users.email==email).first()

    if not is_User:
        return jsonify({"message":"User doesn't exist ! Please Sign up !"}),401
    
    is_password=is_User.check_password(password)

    if not is_password:
        return jsonify({"message":"Wrong password!!"}),401
    
    token=create_access_token(identity=str(is_User.id))
    return jsonify({"message":"User login successfully",
                    "token":token})



