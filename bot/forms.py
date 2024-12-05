from django.contrib.auth.forms import UserCreationForm
from .models import UserRegistration
class Userregistrationform(UserCreationForm):
    class Meta:
        model=UserRegistration
        fields=('user_id','user_name','full_name','phone_number','email')