import io
from PIL import Image
import requests
from sqlalchemy import Column,\
                       Integer
from sqlalchemy_api_handler import humanize

from utils.inflect import inflect_engine
from utils.object_storage import delete_public_object,\
                                 get_public_object_date,\
                                 store_public_object

IDEAL_THUMB_WIDTH = 600

class HasThumbMixin(object):
    thumbCount = Column(Integer(), nullable=False, default=0)

    def delete_thumb(self, index):
        delete_public_object("thumbs", self.thumb_storage_id(index))

    def thumb_date(self, index):
        return get_public_object_date("thumbs", self.thumb_storage_id(index))

    def thumb_storage_id(self, index):
        if self.id is None:
            raise ValueError("Trying to get thumb_storage_id for an unsaved object")
        return inflect_engine.plural(self.__class__.__name__.lower()) + "/"\
                                     + humanize(self.id)\
                                     + (('_' + str(index)) if index > 0 else '')

    def save_thumb(self,
                   thumb,
                   index,
                   image_type=None,
                   no_convert=False,
                   crop=None,
                   symlink_path=None):
        if isinstance(thumb, str):
            if not thumb[0:4] == 'http':
                raise ValueError('Invalid thumb URL for object '
                                 + str(self)
                                 + ' : ' + thumb)
            thumb_response = requests.get(thumb)
            content_type = thumb_response.headers['Content-type']
            if thumb_response.status_code == 200 and\
               content_type.split('/')[0] == 'image':
                thumb = thumb_response.content
            else:
                raise ValueError('Error downloading thumb for object '
                                 + str(self)
                                 + ' status_code: ' + str(thumb_response.status_code))

        if not no_convert:
            thumb_bytes = io.BytesIO(thumb)
            img = Image.open(thumb_bytes)
            img = img.convert('RGB')
            if crop is not None:
                img = img.crop((img.size[0]*crop[0],
                                img.size[1]*crop[1],
                                min(img.size[0]*crop[0]+img.size[1]*crop[2],
                                    img.size[0]),
                                min(img.size[1]*crop[1]+img.size[1]*crop[2],
                                    img.size[1])
                                    ))
            if img.size[0] > IDEAL_THUMB_WIDTH:
                ratio = img.size[1]/img.size[0]
                img = img.resize([IDEAL_THUMB_WIDTH, int(IDEAL_THUMB_WIDTH*ratio)],
                                 Image.ANTIALIAS)
            thumb_bytes.seek(0)
            img.save(thumb_bytes,
                     format='JPEG',
                     quality=80,
                     optimize=True,
                     progressive=True)
            thumb = thumb_bytes.getvalue()

        store_public_object("thumbs",
                            self.thumb_storage_id(index),
                            thumb,
                            "image/" + (image_type or "jpeg"),
                            symlink_path=symlink_path)

        self.thumbCount = max(index+1, self.thumbCount or 0)

        self.__class__.save(self)
