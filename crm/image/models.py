import os
import enum
from flask_admin import form
from crm.db import db, BaseModel, RootModel
from crm.settings import IMAGES_DIR, STATIC_URL_PATH


class Image(db.Model, BaseModel, RootModel):
    __tablename__ = "images"
    name = db.Column(db.String(255))
    path = db.Column(db.String(255))
    contact_id = db.Column(
        db.String(5),
        db.ForeignKey('contacts.id')
    )

    @property
    def imgurl(self):
        return os.path.join(STATIC_URL_PATH, "uploads", "images", self.path)

    @property
    def fullpath(self):
        return os.path.join(IMAGES_DIR, self.path)

    @property
    def as_image(self):
        return '<a href={imgurl}><img width="100" height="100" src="{imgurl}"></img></a>'.format(imgurl=self.imgurl)
        # return os.path.join(IMAGES_DIR, self.path)

    def __str__(self):
        return self.path


# @listens_for(Image, 'after_delete')
# def del_image(mapper, connection, target):
#     if target.path:
#         # Delete image
#         try:
#             os.remove(op.join(file_path, target.path))
#         except OSError:
#             pass

#         # Delete thumbnail
#         try:
#             os.remove(op.join(file_path,
#                               form.thumbgen_filename(target.path)))
#         except OSError:
#             pass
