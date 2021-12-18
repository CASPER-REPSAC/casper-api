from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from managing.views import tester, search_all

admin.autodiscover()


urlpatterns = [
    url('admin/', admin.site.urls),
    # GET, POST uri
    # path('', activity_list),
    # path('api/w00/activities', activity_list),
    #path('api/w00/activities/', ActivityViewSet),
    #path('api/activities', activity_list),
    
   
    #Search
    path('api/search/<str:keyword>/', search_all),

    #test
    path('api/test/',tester),

    #Activity
    path('api/w00/', include('activity.urls')),

    #Chapter
    path('api/activities/', include('managing.urls')),

    #JWT Verify
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #OAuth
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
]