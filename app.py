from app import create_app, db
from app.config import Config

app = create_app(config_class=Config)  # Pass as keyword argument






if __name__ == '__main__':
    with app.app_context():
        from app.models import User, Resume
        db.create_all()
    app.run(debug=True)