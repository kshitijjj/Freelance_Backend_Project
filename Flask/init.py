from flask import Flask
from config import db,SQLALCHEMY_DATABASE_URI,SQLALCHEMY_TRACK_MODIFICATIONS,SECRET_KEY
from flask_jwt_extended import JWTManager
from Routes.auth import auth_bp
from Models.Users import Users
from Models.Jobs import Jobs
from Routes.users import user_bp

jwt=JWTManager()

def create_app():
    app=Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI']=SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY']=SECRET_KEY

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    with app.app_context():
        db.create_all()

    return app

if __name__=="__main__":
    app=create_app()
    app.run(debug=True)
