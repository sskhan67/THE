"""Routes for user authentication."""
from flask import Blueprint, jsonify, request
from flask_login import login_user
from models import User, ACCESS
from __init__ import login_manager, db
from functools import wraps

# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__
)


### custom wrap to determine access level ###
def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = {}
            email = request.headers.get('email')
            user = User.query.filter_by(email=email).first()
            if not user:
                response['error'] = f"Unable to find user with email {email}"
                return jsonify(response)
            elif not user.check_password(request.headers.get('password')):  # the user is not logged in
                response['error'] = f"Unable to Validate Password"
                return jsonify(response)
            if "|" in access_level:
                if not (user.allowed(access_level.split("|")[0]) and user.allowed(access_level.split("|")[1])):
                    response['error'] = 'You do not have access to this resource.'
                    return jsonify(response)
            elif not user.allowed(access_level):
                response['error'] = 'You do not have access to this resource.'
                return jsonify(response)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    response = {}
    data = request.get_json()
    email = data['email']
    user = User.query.filter_by(email=email).first()
    if user and user.is_authenticated:
        response['text'] = f"user {user.username} already logged in "
        return jsonify(response)
    elif user and user.check_password(password=data['password']):
        login_user(user)
        response['text'] = f"logged in {user.username}"
        return jsonify(response)
    else:
        response['error'] = "Unable to find user"
        return jsonify(response)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User sign-up page.

    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    response = {}
    data = request.get_json()
    email = data['email']
    existing_user = User.query.filter_by(email=email).first()
    user = User()
    if not existing_user:
        user.email = data['email']
        user.username = data['name']
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()  # Create new user
        login_user(user)  # Log in as newly created user
        response['text'] = f"User Signed up {user.email}"
        return jsonify(response)
    else:
        response['text'] = f"User {existing_user.email} already exists"
        return jsonify(response)


@login_manager.unauthorized_handler
def unauthorized():
    response = {}
    """Redirect unauthorized users to Login page."""
    response['error'] = 'You must be logged in to view that page.'
    return jsonify(response)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@auth_bp.route('/delete_user')
@requires_access_level(ACCESS['admin'])
def delete_user():
    response = {}
    data = request.json()
    email = data['email']
    existing_user = User.query.filter_by(email=email).first()
    db.session.delete(existing_user)
    db.session.commit()
    response['message'] = f'User with email {email} has been deleted.'
    return jsonify(response)


# control panel
@auth_bp.route('/control_panel')
@requires_access_level('admin')
def control_panel():
    all_users = User.query.all()
    serialized_users = []
    for usr in all_users:
        serialized_users.append(usr.serialize())
    return jsonify(serialized_users)
