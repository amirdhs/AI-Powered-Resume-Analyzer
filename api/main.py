from flask_migrate import Migrate
from api.app import create_app, db
from api.app.config import Config

app = create_app(config_class=Config)
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)