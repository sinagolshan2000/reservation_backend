import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')

# Initialize Django
django.setup()

from loaders.loaders import DataLoder


def run():
    DataLoder().load()
