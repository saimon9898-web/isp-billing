from app import app
from models import db, User, Plan, Transaction


def run_daily_billing():
    with app.app_context():
        print("--- Starting Daily Billing Run ---")

        # Get all active users
        users = User.query.filter_by(is_active=True).all()

        for user in users:
            # Assume everyone is on Plan 1 ($50/mo) for this MVP
            # In a real app, we'd fetch user.plan.price
            daily_cost = 50.0 / 30.0

            user.balance -= daily_cost

            # Log the charge (silent log, rarely shown to user unless requested)
            # trans = Transaction(user_id=user.id, amount=-daily_cost, description="Daily Charge")
            # db.session.add(trans)

            print(
                f"Charged {user.username}: -${daily_cost:.2f}. New Balance: {user.balance:.2f}")

            # DISCONNECT LOGIC
            if user.balance < -10.0:  # Allow $10 credit limit
                user.is_active = False
                print(
                    f"!!! SUSPENDING USER: {user.username} (Insufficient Funds)")
                # HERE: You would add code to send a 'Kill' command to the router (CoA)

        db.session.commit()
        print("--- Billing Run Complete ---")


if __name__ == "__main__":
    run_daily_billing()
