from flask import Blueprint, jsonify, request
from __init__ import db
from auth import requires_access_level


# Blueprint Configuration
from models import Company, User, user_companies

company_bp = Blueprint(
    'company_bp', __name__
)

@company_bp.route('/create-company', methods=['GET', 'POST'])
@requires_access_level(access_level='admin')
def create_company():
    response = {}
    data = request.get_json()
    name = data['name']
    existing_company = Company.query.filter_by(name=name).first()
    if not existing_company:
        com = Company()
        com.name = name
        db.session.add(com)
        db.session.commit()
        response['text'] = f"Company created {com.name}"
        return jsonify(response)
    else:
        response['text'] = f"company already exists {name}"
        return jsonify(response)


@company_bp.route('/delete-company', methods=['GET', 'POST'])
@requires_access_level("admin")
def delete_company():
    response = {}
    data = request.get_json()
    name = data['name']
    company_exists = Company.query.filter_by(name=name).first()
    if company_exists:
        db.session.delete(company_exists)
        db.session.commit()  # Create new user
        response['text'] = f"Company Deleted {company_exists.name}"
        return jsonify(response)
    else:
        response['text'] = f"Company doesn't exist with name {name}"
        return jsonify(response)

@company_bp.route('/add-company-user', methods=['GET', 'POST'])
@requires_access_level("admin")
def add_company_user():
    response = {}
    data = request.get_json()
    company_name = data['company_name']
    email = data['email']
    company_exists = Company.query.filter_by(name=company_name).first()
    user = User.query.filter_by(email=email).first()
    if company_exists and user:
        user.companies.append(company_exists)
        db.session.add(user)
        db.session.commit()
        response['text'] = f"Company {company_exists.name} added to user {user.email}"
        return jsonify(response)
    elif not user:
        response['text'] = f"User doesn't exist with email {email}"
        return jsonify(response)
    elif not company_exists:
        response['text'] = f"Company doesn't exist with name {company_name}"
        return jsonify(response)

@company_bp.route('/get-user-companies', methods=['GET', 'POST'])
@requires_access_level("admin|company_list")
def get_user_companies():
    response = {}
    data = request.get_json()
    email = data['email']
    user = User.query.filter_by(email=email).first()
    if user:
        all_companies = user.companies
        company_names = []
        for company in all_companies:
            company_names.append(company.name)
        response['text'] = f"User {email} has access to  {' | '.join(company_names)} companies"
        return jsonify(response)
    elif not user:
        response['text'] = f"User doesn't exist with email {email}"
        return jsonify(response)


@company_bp.route('/get-company-users', methods=['GET', 'POST'])
@requires_access_level("admin")
def get_company_users():
    response = {}
    data = request.get_json()
    company_name = data['name']
    company = Company.query.filter_by(name=company_name).first()
    if company:
        all_users = db.session.query(user_companies).filter_by(company_id=company.id).all()
        user_email = []
        for user in all_users:
            user_email.append(str(user[0]))
        response['text'] = f"company {company_name} is accessible user ids to  {' | '.join(user_email)} users"
        return jsonify(response)
    elif not company:
        response['text'] = f"User doesn't exist with email {company_name}"
        return jsonify(response)



