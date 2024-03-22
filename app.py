from flask_admin import Admin
from flask import Flask
from flask_mongoengine import MongoEngine
from views import ProductView

app = Flask(__name__)
app.config["MONGODB_HOST"] = "mongodb+srv://carbonitedb:MVsMrhy80saYhOPX@cluster0.w4bq05q.mongodb.net/"
app.config["SECRET_KEY"] = "sigh"
try:
    mongodb = MongoEngine()
    mongodb.init_app(app=app)
    print("mongo connection initiated successfully")
except:
    print("ye 3alayna")

from models import InventoryManager

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'pulse'
app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True

admin = Admin(app, name='Fabric Inv Management Tool', template_mode='bootstrap4')

# Add administrative views here

admin.add_view(ProductView(InventoryManager))
if __name__ == '__main__':
    app.run()
