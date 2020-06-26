from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User
# Create your views here.

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')
    else:
        form = UserCreationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/form.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        # AuthenticationForm은 ModelForm이 아닌 Form 상속
        # 별도로 정의된 Model이 없다는 뜻
        # 그래서 넘겨주는 인자가 달라진다.
        if form.is_valid():
                # login_form이 가지고 있는 user정보를 가지고 와서 넘겨 주어야 한다.
                # 로그인은 DB에 뭔가 작성하는 것은 동일하지만, 연결된 모델이 있는건
                # 아니다. 그럼 무엇을 확인해야 하는가?
                # 세션과 유저 정보
            auth_login(request, form.get_user())
            return redirect('articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/form.html', context)

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
        # form = UserChangeForm(data=request.POST, instance=request.user)
        form = CustomUserChangeForm(data=request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            return redirect('articles:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form' : form
    }
    return render(request, 'accounts/form.html', context)

@login_required   
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # 기존 세션 유지 메서드이다.
            update_session_auth_hash(request, user)
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form' : form
    }
    return render(request, 'accounts/form.html', context)


@login_required
def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    context = {
        'person' : person
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def follow(request, user_pk):
    # person에 담긴 user_pk값을 가진 유저는
    # 프로필의 주인이다.
    # request.user는 나. 요청을 보내온 사용자이다.
    person = get_object_or_404(get_user_model(), pk=user_pk)
    user = request.user
    if user in person.followers.all():
        person.followers.remove(user)
    else:
        person.followers.add(user)
    return redirect('accounts:profile', person.username )
