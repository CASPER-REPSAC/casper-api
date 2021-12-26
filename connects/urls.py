from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.views.generic import RedirectView
from managing.views import search_all
from activity.member_management import ownActivity, containedActivity_new,  containedActivity


admin.autodiscover()

sch_urlpatterns = [
    #url('admin/', admin.site.urls),

    # ownActivity
    path('api/user/<int:pk>/', ownActivity),

    # contained Activitiy
    path('api/user/contained/', containedActivity),

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

schema_view = get_schema_view( 
    openapi.Info( 
            title="Django API", 
            default_version='v1', 
            terms_of_service="https://www.google.com/policies/terms/", 
            ), 
            public=True, 
            permission_classes=(permissions.AllowAny,), 
            patterns=sch_urlpatterns, 
        )

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


    # API DOC
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'), 
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), 
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]