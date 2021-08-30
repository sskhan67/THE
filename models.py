"""Database models."""
from __init__ import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


ACCESS = {
    'guest': 0,
    'user': 1,
    'admin': 2
}

user_companies = db.Table(
    "user_companies",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("company_id", db.Integer, db.ForeignKey("company.id")),
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    created_on = db.Column(db.DateTime, index=False,  unique=False, nullable=True)
    last_login = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    roles = db.Column(db.String, index=False, unique=False, nullable=True)
    permissions = db.Column(db.String, index=False, unique=False, nullable=True)
    password = db.Column(db.String(128))
    companies = db.relationship("Company", secondary=user_companies)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def set_permissions(self, permission):
        if type(permission) == list and self.permissions:
            all_permissions = self.permissions.split("|")
            all_permissions.extend(permission)
            all_permissions = list(set(all_permissions))
            self.permissions = "|".join(all_permissions)
        elif type(permission) == str and self.permissions:
            all_permissions = self.permissions.split("|")
            all_permissions.append(permission)
            all_permissions = list(set(all_permissions))
            self.permissions = "|".join(all_permissions)
        elif type(permission) == list and not self.permissions:
            all_permissions = permission
            all_permissions = list(set(all_permissions))
            self.permissions = "|".join(all_permissions)
        elif type(permission) == str and not self.permissions:
            self.permissions = permission

    def get_permissions(self):
        return self.permissions.split("|")

    def set_role(self, roles):
        if type(roles) == list and self.roles:
            all_roles = self.roles.split("|")
            all_roles.extend(roles)
            all_roles = list(set(all_roles))
            self.roles = "|".join(all_roles)
        elif type(roles) == str and self.roles:
            all_roles = self.roles.split("|")
            all_roles.append(roles)
            all_roles = list(set(all_roles))
            self.roles = "|".join(all_roles)
        elif type(roles) == list and not self.roles:
            all_roles = roles
            all_roles = list(set(all_roles))
            self.roles = "|".join(all_roles)
        elif type(roles) == str and not self.roles:
            self.roles = roles

    def get_roles(self):
        return self.roles.split("|")

    def allowed(self, role):
        if self.roles:
            return role in self.roles.split("|") or role in self.permissions.split("|")
        else:
            return False


    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)


    def serialize(self):
        return {"email": self.email,
                "username": self.username,
                "role": self.roles}

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
