from app import app
from models import InventoryManager

with app.app_context():
    for item in InventoryManager.objects():
        item.quantity = 24
        item.save()