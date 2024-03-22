import datetime
import uuid

from app import mongodb


def generate_uuid():
    return str(uuid.uuid4())


class InventoryManager(mongodb.DynamicDocument):
    meta = {
        "collection": "inventory_manager"
    }

    product_id = mongodb.StringField(required=True, unique=True, default=generate_uuid)
    name = mongodb.StringField(default="")
    type = mongodb.StringField(default="حرير")
    product_image_binary = mongodb.BinaryField(default=b'')
    date_created = mongodb.DateTimeField(default=datetime.datetime.utcnow())
    date_modified = mongodb.DateTimeField()
    total_square_meters = mongodb.FloatField(default=0)
    remaining_meters = mongodb.FloatField(default=0)
    cost = mongodb.FloatField(default=0)
    cost_m2 = mongodb.FloatField(default=0)
