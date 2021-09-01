import os
from django.conf.global_settings import FILE_UPLOAD_MAX_MEMORY_SIZE
import datetime
import uuid

MEDIA_URL = '/media'
MEDIA_ROOT = os.path.join('','media')

def file_upload_path(filename):
    ext = filename.split('.')[-1]
    d = datetime.datetime.now()
    filepath = d.strftime('%Y\\%m\\%d')
    suffix = d.strftime("%Y%m%d%H%M%S")
    filename = "%s_%s.%s"%(uuid.uuid4().hex, suffix, ext)
    return os.path.join(MEDIA_ROOT, filepath, filename)

def file_upload_path_for_db(instance, filename):
    return file_upload_path(filename)
