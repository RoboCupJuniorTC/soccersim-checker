from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.views import ModelView, CompactCRUDMixin
from app.models import Upload

from . import appbuilder, db

"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""


class UploadModelView(CompactCRUDMixin, ModelView):
    datamodel = SQLAInterface(Upload)
    base_permissions = ['can_add', 'can_list', 'can_show', 'can_download']
    base_order = ('created_on', 'desc')
    list_template = 'list_uploads.html'

    label_columns = {
        "file_name": "File Name",
        "download": "Download",
        "custom_status": "Status"
    }

    add_columns = ["file", "description"]
    edit_columns = ["file", "description"]
    list_columns = ["created_by", "created_on",
                    "file_name", "description", "custom_status", "download"]
    show_columns = ["created_by", "created_on",
                    "file_name", "description", "custom_status", "download"]


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html",
            base_template=appbuilder.base_template,
            appbuilder=appbuilder
        ),
        404,
    )


db.create_all()
appbuilder.add_view(
    UploadModelView, "List Uploads", icon="fa-table", category="Code Uploads"
)
