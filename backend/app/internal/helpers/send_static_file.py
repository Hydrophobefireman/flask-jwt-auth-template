from flask import send_from_directory

from app.settings import app_settings

ONE_YEAR_IN_SECONDS = 365 * 86400


def send_static_file(file_name: str, max_age=ONE_YEAR_IN_SECONDS):
    return send_from_directory(app_settings.static_dir, file_name, max_age=max_age)
