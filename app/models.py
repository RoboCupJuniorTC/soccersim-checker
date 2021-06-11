from flask import Markup, url_for, g
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Enum
from flask_appbuilder.models.mixins import AuditMixin, FileColumn
from flask_appbuilder.filemanager import get_file_original_name
from flask_appbuilder.models.decorators import renders
from . import app

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""


class AuditMixinExtra(AuditMixin):
    """to work with this app's database permitting edits by 'unknown' user
    """
    def get_user_id(cls):
        try:
            return g.user.id
        except Exception:
            return 1


class Upload(AuditMixinExtra, Model):
    __tablename__ = "upload"
    id = Column(Integer, primary_key=True)
    file = Column(FileColumn, nullable=False)
    status = Column(Enum("Uploaded", "InProgress", "Simulated"),
                    server_default="Uploaded")
    description = Column(String(150))
    match_id = Column(String(150))

    def __repr__(self):
        return f'<Upload({self.file_name()}, status={self.status})>'

    def download(self):
        return Markup(
            '<a href="'
            + url_for("UploadModelView.download",
                      filename=str(self.file))
            + '">Download</a>'
        )

    def file_name(self):
        return get_file_original_name(str(self.file))

    @renders('status')
    def custom_status(self):
        status_to_bnt = {
            'Uploaded': 'label-default',
            'InProgress': 'label-warning',
            'Simulated': 'label-success'
        }

        return Markup(
            f'<span class="label {status_to_bnt[self.status]}">'
            f'{self.status}'
            '</span>'
        )

    def match_link(self):
        # If output_dir was not set yet or is empty, just return that
        if not self.match_id or len(self.match_id) == 0:
            return Markup('')

        return Markup(
            f'<a href="{app.config["OUTPUTS_URL"]}/{self.match_id}">'
            ' Check output '
            '</a>'
        )
