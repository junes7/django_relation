from django.urls import path
from . import views1

app_name = "accounts"
urlpatterns = [
    path('signup/', views1.signup, name="signup"),
    path('login/', views1.login, name="login"),
    path('logout/', views1.logout, name="logout"),
    path('delete/', views1.delete, name="delete"),
    path('update/', views1.update, name="update"),
    path('password/', views1.change_password, name="change_password"),
    path('follow/<int:user_pk>/', views1.follow, name="follow"),
    # 문자열만 받고 싶으면 가장 밑에 이 경로를 만들어야 한다.
    path('<str:username>/', views1.profile, name="profile"),
]
