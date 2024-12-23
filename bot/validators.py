from django.core.exceptions import ValidationError
import os


def validate_image(file):
    allowed_extensions=('.jpg','.gif','.png','.jpeg')
    get_extension=os.path.splitext(file.name)[1]
    if get_extension not in allowed_extensions:
        raise ValidationError("Enter a valid file")
    

def validate_pdf(file):
    get_extension=os.path.splitext(file.name)[1]
    if get_extension != '.pdf':
        raise ValidationError('Please provide a valid file')
