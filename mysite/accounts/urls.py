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
]
