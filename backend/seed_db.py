"""
Command-line helper to create a fresh SQLite database with
demo-ready data in a single run.
"""
from app import app, db
from demo_data import seed_demo_data


def seed_database():
    """Drop existing demo entities (except admin) and repopulate data."""
    with app.app_context():
        db.create_all()
        seed_demo_data(force_reset=True)


if __name__ == '__main__':
    seed_database()
    print("Demo database ready. Use the credentials listed in README.md to sign in.")

