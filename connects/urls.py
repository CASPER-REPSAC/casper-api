from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.views.generic import RedirectView
from managing.views import search_all
from activity.member_management import ownActivity, containedActivity_new,  containedActivity

admin.autodiscover()

urlpatterns = [
    # path('api-auth/', include('rest_framework.urls'), name='api-login'),
    # path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    #url('admin/', admin.site.urls),

    # ownActivity
    path('api/user/<int:pk>/', ownActivity),

    # contained Activitiy
    path('api/user/contained/', containedActivity),
    path('api/user/contained_new/', containedActivity_new),


    # Search
    path('api/search/', search_all),

    # Activity
    path('api/w00/', include('activity.urls')),

    # Chapter
    path('api/activities/', include('managing.urls')),

    # JWT Verify
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # OAuth
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
]
