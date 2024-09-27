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
        """
        A function to generate a name for avatar image

        :param email: EmailStr: Specify the email address of the user
        :return: str: return a sting with generated name
        """
        name = hashlib.sha256(email.encode('utf-8')).hexdigest()[:12]
        return f'hw13/{name}'

    @staticmethod
    def upload(file, public_id: str):
        """
        Upload a file to Cloudinary with a given public ID.

        :param file: Any - The file to be uploaded.
        :param public_id: str - The public ID for the avatar.
        :return: dict - A dictionary containing the response from Cloudinary.
        """
        r = cloudinary.uploader.upload(file, public_id=public_id, overwrite=True)
        return r

    @staticmethod
    def get_url_for_avatar(public_id, r):
        """
        Get the URL for an avatar image from Cloudinary.

        :param public_id: str - The public ID of the avatar.
        :param r: dict - The response dictionary from the Cloudinary upload.
        :return: str - The URL for the avatar image.
        """
        src_url = cloudinary.CloudinaryImage(public_id) \
            .build_url(width=250, height=250, crop='fill', version=r.get('version'))
        return src_url