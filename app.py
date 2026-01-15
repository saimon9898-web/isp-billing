from flask import Flask, render_template, request, redirect, url_for
from models import db, User, Plan, Transaction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret_key_here'

db.init_app(app)

# Create DB tables if they don't exist
with app.app_context():
    db.create_all()

# --- ROUTES ---


@app.route('/')
def dashboard():
    users = User.query.all()
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    return render_template('dashboard.html', users=users, stats={'total': total_users, 'active': active_users})


@app.route('/add_user', methods=['POST'])
def add_user():
    # Simple logic to add a new customer
    username = request.form['username']
    full_name = request.form['full_name']

    # Assign a default plan (ID 1) for demo
    new_user = User(username=username, password="password123",
                    full_name=full_name, plan_id=1)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('dashboard'))


@app.route('/pay/<int:user_id>', methods=['POST'])
def add_payment(user_id):
    # Manual payment entry by Admin
    amount = float(request.form['amount'])
    user = User.query.get(user_id)

    user.balance += amount

    # Log the transaction
    trans = Transaction(user_id=user.id, amount=amount,
                        description="Manual Payment")
    db.session.add(trans)

    # Auto-activate if balance is positive
    if user.balance >= 0:
        user.is_active = True

    db.session.commit()
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
