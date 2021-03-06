from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserChangeForm
# Create your views here.

def signup(request):
    if request.method == "POST":
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            auth_login(request, user)
            return redirect('articles:index')
    else:
        signup_form = UserCreationForm()
    context = {
        'signup_form' : signup_form
    }
    return render(request, 'accounts/signup.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == "POST":
        login_form = AuthenticationForm(request, request.POST)
        # AuthenticationForm은 ModelForm이 아닌 Form 상속
        # 별도로 정의된 Model이 없다는 뜻
        # 그래서 넘겨주는 인자가 달라진다.
        if login_form.is_valid():
                # login_form이 가지고 있는 user정보를 가지고 와서 넘겨 주어야 한다.
                # 로그인은 DB에 뭔가 작성하는 것은 동일하지만, 연결된 모델이 있는건
                # 아니다. 그럼 무엇을 확인해야 하는가?
                # 세션과 유저 정보
            auth_login(request, login_form.get_user())
            return redirect('articles:index')
    else:
        login_form = AuthenticationForm()
    context = {
        'login_form' : login_form
    }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('articles:index')

@require_POST
def delete(request):
    # if request.method == "POST"
    request.user.delete()
    return redirect('articles:index')

@login_required
def update(request):
    # 먼저 get방식부터 작성해서 form을 보고 POST방식의 코드를 구현할 것!!
    # instance : 변경할 대상(User 객체)을 담는 인자
    # data : 변경할 정보를 담는 인자
    if request.method == "POST":
        # user_change_form = UserChangeForm(data=request.POST, instance=request.user)
        user_change_form = CustomUserChangeForm(data=request.POST, instance=request.user)
        if user_change_form.is_valid():
            user = user_change_form.save()
            return redirect('articles:index')
    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
    context = {
        'user_change_form' : user_change_form
    }
    return render(request, 'accounts/update.html', context)

@login_required   
def change_password(request):
    if request.method == "POST":
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            # 기존 세션 유지 메서드이다.
            update_session_auth_hash(request, user)
            return redirect('articles:index')
    else:
        password_change_form = PasswordChangeForm(request.user)
    context = {
        'password_change_form' : password_change_form
    }
    return render(request, 'accounts/change_password.html', context)
