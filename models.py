from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# 1. The Internet Plans (e.g., "100Mbps - $50")


class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    speed_mbps = db.Column(db.Integer, nullable=False)

# 2. The Customer (Your Subscriber)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True,
                         nullable=False)  # For Radius/PPPoE
    password = db.Column(db.String(80), nullable=False)
    full_name = db.Column(db.String(120))
    balance = db.Column(db.Float, default=0.0)
    is_active = db.Column(db.Boolean, default=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'))

    plan = db.relationship('Plan', backref=db.backref('users', lazy=True))

# 3. Transaction History (Payments & Charges)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Negative for charges, Positive for payments
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)
