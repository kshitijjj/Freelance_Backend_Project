from flask_jwt_extended import get_jwt,jwt_required
from flask import jsonify
from functools import wraps

def admin_required(fn):
    @wraps(fn)
    def check_role(*args,**kwargs):
        role=get_jwt()
        if role['role']!="admin":
            return jsonify({"message":"Access Denied"}),403
        return fn(*args,**kwargs)
    return check_role
