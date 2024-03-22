import datetime
import io
from flask_admin.contrib.mongoengine import ModelView
from flask_wtf.file import FileField
from markupsafe import Markup
import base64
from PIL import Image


class ProductView(ModelView):
    page_size = 50
    column_searchable_list = ['name']
    create_modal = True
    edit_modal = True
    can_view_details = True

    column_formatters = {
        'product_image_binary': lambda v, c, m, p: Markup(
            '<img width="200" height="200" '
            'src="data:image/jpeg;base64,{}">'.format(base64.b64encode(m.product_image_binary).decode('utf-8'))
        ),
        'date_modified': lambda v, c, m, p: Markup(
            '<span style="font-weight:bold;">{}</span>'.format(
                m.date_modified.strftime('%d.%m.%Y') if m.date_modified else None)
        ),
        'date_created': lambda v, c, m, p: Markup(
            '<span style="font-weight:bold;">{}</span>'.format(
                m.date_created.strftime('%d.%m.%Y') if m.date_created else None)
        ),
        'type': lambda v, c, m, p: Markup(
            '<span style="font-weight:bold;">{}</span>'.format(m.type)
        ),
        'cost': lambda v, c, m, p: Markup(
            '<span style="font-weight:bold; color:orange">{}</span>'.format(m.cost)
        ),
        'cost_m2': lambda v, c, m, p: Markup(
            '<span style="font-weight:bold; color:purple">{}</span>'.format(m.cost_m2)
        ),
        'remaining_meters': lambda v, c, m, p: Markup(
            '<span style="font-weight:bold; color:{}">{}</span>'.format("red" if m.remaining_meters < 3 else "blue",
                                                                        m.remaining_meters)
        ),
    }
    column_list = [
        'product_image_binary',
        'product_id',
        'name',
        'date_created',
        'cost',
        'cost_m2',
        'type',
        'date_modified',
        'remaining_meters'
    ]

    column_labels = {
        'product_image_binary': "Product Picture",
        'product_id': "Product ID",
        'name': "Product Name",
        'cost': "Product Cost USD",
        'type': "Product type"
    }
    column_filters = [
        'product_id',
        'name',
        'cost',
        'remaining_meters',
        'cost_m2'
    ]
    form_extra_fields = {
        'product_image_binary': FileField('Image')
    }
    form_excluded_columns = [
        'product_id',
        'date_modified',
        'date_created'
    ]

    def __init__(self, model, name=None,
                 category=None, endpoint=None, url=None, static_folder=None,
                 menu_class_name=None, menu_icon_type=None, menu_icon_value=None):
        super().__init__(model, name, category, endpoint, url, static_folder, menu_class_name, menu_icon_type,
                         menu_icon_value)
        self.remaining_meters = None

    def edit_form(self, obj=None):
        try:
            self.remaining_meters = obj.remaining_meters
        except AttributeError:
            pass

        return ModelView.edit_form(self, obj)

    def on_model_change(self, form, model, is_created):
        if self.remaining_meters != model.remaining_meters:
            model.date_modified = datetime.datetime.utcnow()
        if form.product_image_binary.data and not isinstance(form.product_image_binary.data, bytes):
            image_binary_data = form.product_image_binary.data.read()
            image = Image.open(io.BytesIO(image_binary_data))
            width, height = image.size
            if width < 200 or height < 200:
                raise ValueError('Image size is too small')
            if width > height:
                new_size = (height, height)
            else:
                new_size = (width, width)

                # Calculate crop box coordinates
            left = (width - new_size[0]) // 2
            top = (height - new_size[1]) // 2
            right = left + new_size[0]
            bottom = top + new_size[1]

            # Crop the image
            image = image.crop((left, top, right, bottom))
            # Create in-memory buffer
            output_buffer = io.BytesIO()
            image.save(output_buffer, format='PNG')  # Save using original format

            # Get binary data from buffer
            manipulated_binary_data = output_buffer.getvalue()
            model.product_image_binary = manipulated_binary_data
        model.save()
