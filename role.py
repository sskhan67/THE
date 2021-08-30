from flask import Blueprint, jsonify, request
from __init__ import db
from auth import requires_access_level


# Blueprint Configuration
from models import User

role_bp = Blueprint(
    'role_bp', __name__
)

@role_bp.route('/create-admin', methods=['POST'])
def create_admin():
    response = {}
    existing_user = User.query.filter_by(email="test@test.com").first()
    if not existing_user:
        user = User()
        user.email = "test@test.com"
        user.username = "test"
        user.set_password("password")
        user.set_role("admin")
        user.set_permissions("company_list")
        db.session.add(user)
        db.session.commit()
        response['text'] = 'Admin User Created'
        return jsonify(response)
    else:
        response['text'] = 'user already exists'
        return jsonify(response)



@role_bp.route('/create-role', methods=['GET', 'POST'])
@requires_access_level(access_level='admin')
def create_role():
    response = {}
    data = request.get_json()
    email = data['email']
    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        user_exists.set_role(data['role'])
        db.session.commit()
        response['text'] = f"Role Added {data['role']} to user {email}"
        return jsonify(response)
    else:
        response['text'] = f"User doesn't exist {email}"
        return jsonify(response)


@role_bp.route('/delete-role', methods=['GET', 'POST'])
@requires_access_level("admin")
def delete_role():
    response = {}
    data = request.get_json()
    email = data['email']
    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        roles = user_exists.get_roles()
        role = data['role']
        if role in roles:
            roles.remove(role)
        else:
            response['text'] = f"Role doesn't exist in user {role}"
            return jsonify(response)
        user_exists.roles = "|".join(roles)
        db.session.commit()  # Create new user
        response['text'] = f"Role Removed from user {user_exists.email}"
        return jsonify(response)
    else:
        response['text'] = f"User doesn't exist with email {email}"
        return jsonify(response)


@role_bp.route('/create-permissions', methods=['GET', 'POST'])
@requires_access_level(access_level='admin')
def create_permissions():
    response = {}
    data = request.get_json()
    email = data['email']
    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        user_exists.set_permissions(data['permission'])
        db.session.commit()
        response['text'] = f"Permission Added {data['permission']} to user {email}"
        return jsonify(response)
    else:
        response['text'] = f"User doesn't exist {email}"
        return jsonify(response)


@role_bp.route('/delete-permissions', methods=['GET', 'POST'])
@requires_access_level("admin")
def delete_permissions():
    response = {}
    data = request.get_json()
    email = data['email']
    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        permissions = user_exists.get_permissions()
        permission = data['permission']
        if permission in permissions:
            permissions.remove(permission)
        else:
            response['text'] = f"Permission doesn't exist in user {permission}"
            return jsonify(response)
        user_exists.permissions = "|".join(permissions)
        db.session.commit()  # Create new user
        response['text'] = f"Permission Removed from user {user_exists.email}"
        return jsonify(response)
    else:
        response['text'] = f"User doesn't exist with email {email}"
        return jsonify(response)

