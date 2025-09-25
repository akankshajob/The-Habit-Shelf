from app import create_app, db
from app.models import User, Habit  # make sure you have these models in app/models.py

# Create Flask app
app = create_app()

with app.app_context():
    print("✅ Connected to database")

    # Show all tables
    tables = db.engine.table_names()
    print("📂 Tables in DB:", tables)

    # Example: show all users
    users = User.query.all()
    print("👤 Users in DB:", users)

    # Example: show all habits
    habits = Habit.query.all()
    print("📖 Habits in DB:", habits)
