import hashlib

import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os
load_dotenv()


class CloudImage:
    cloudinary.config(
        cloud_name=os.getenv('API_NAME'),
        api_key=os.getenv('API_KEY'),
        api_secret=os.getenv('API_SECRET'),
        secure=True
    )

    @staticmethod
    def generate_name_avatar(email: str):
        name = hashlib.sha256(email.encode('utf-8')).hexdigest()[:12]
        return f'hw13/{name}'

    @staticmethod
    def upload(file, public_id: str):
        r = cloudinary.uploader.upload(file, public_id=public_id, overwrite=True)
        return r

    @staticmethod
    def get_url_for_avatar(public_id, r):
        src_url = cloudinary.CloudinaryImage(public_id) \
            .build_url(width=250, height=250, crop='fill', version=r.get('version'))
        return src_url