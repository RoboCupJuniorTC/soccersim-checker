from flask import Markup, url_for
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Enum
from flask_appbuilder.models.mixins import AuditMixin, FileColumn
from flask_appbuilder.filemanager import get_file_original_name
from flask_appbuilder.models.decorators import renders

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""


class Uploads(AuditMixin, Model):
    __tablename__ = "uploads"
    id = Column(Integer, primary_key=True)
    file = Column(FileColumn, nullable=False)
    status = Column(Enum("Uploaded", "In progress", "Simulated"),
                    server_default="Uploaded")
    description = Column(String(150))

    def download(self):
        return Markup(
            '<a href="'
            + url_for("UploadsModelView.download",
                      filename=str(self.file))
            + '">Download</a>'
        )

    def file_name(self):
        return get_file_original_name(str(self.file))

    @renders('status')
    def custom_status(self):
        status_to_bnt = {
            'Uploaded': 'label-default',
            'In progress': 'label-warning',
            'Simulated': 'label-success'
        }

        return Markup(
            f'<span class="label {status_to_bnt[self.status]}">'
            f'{self.status}'
            '</span>'
        )
