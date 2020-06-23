from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        # 밑의 메소드는 활성화된 user model이다.
        model = get_user_model()
        fields = ['email','first_name','last_name']

