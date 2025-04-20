from flask_migrate import Migrate
from api.app import create_app, db
from api.app.config import Config

app = create_app(config_class=Config)
migrate = Migrate(app, db)

# Optional: If you want to auto-create tables during Vercel deployment
with app.app_context():
    db.create_all()

