from django.urls import path
from accounts.views import *
from accounts import views
from .views import *

urlpatterns = [

     #path('google/', GoogleLoginApi.as_view(), name='google_login'), 
     #path('google/callback/', GoogleSigninCallBackApi.as_view(), name='google_login_callback'),


     #path('create/', CreateAccount.as_view(), name="create_user"),
     #path('all/', AllUsers.as_view(), name="all"),
     #path('currentUser/', CurrentUser.as_view(), name="current"),

     # path('kakao/login/', views.kakao_login, name='kakao_login'),
     # path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
     # path('kakao/login/finish/', views.KakaoLogin.as_view(), name='kakao_login_todjango'),
     #
     # path('github/login/', views.github_login, name='github_login'),
     # path('github/callback/', views.github_callback, name='github_callback'),
     # path('github/login/finish/', views.GithubLogin.as_view(),name='github_login_todjango'),
     path('tokentest/', views.access_token_receive, name='token_test'),
     path('google/login/', views.google_login, name='google_login'),
     path('google/callback/', views.google_callback, name='google_callback'),
     path('google/login/finish/', views.GoogleLogin.as_view(),name='google_login_todjango'),
]
