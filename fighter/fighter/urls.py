"""fighter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers
from contest import views
from rest_framework_extensions.routers import ExtendedSimpleRouter
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

router = ExtendedSimpleRouter()
event_router = router.register(r'events', views.EventViewSet)
event_router.register(
                r'bouts',
                views.BoutViewSet,
                basename='events-bout',
                parents_query_lookups=['event']
            )

router.register(r'fighters', views.FighterViewSet)
router.register(r'entries', views.EntryViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/registration/', include('rest_auth.registration.urls')),
    path('api/latest_event/', views.EventViewSet.as_view({'get': 'get_latestevent'}), name='latest_event'),
    path('api/check_user_already_taken', views.EntryViewSet.as_view({'get': 'check_user_already_taken'}), name='check_user_already_taken'),
    path('api/entries/save/', views.EntryViewSet.as_view({'post': 'save_entries'}), name='save_entries'),
    path('api/entries/contest', views.EntryViewSet.as_view({'get': 'get_latestContest'}), name='contest'),
    path('api/entries/score_by_user', views.EntryViewSet.as_view({'get': 'get_score_by_user'}), name='get_score_by_user'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
     # JWT auth
    # url(r'^api/v1/auth/obtain_token/', obtain_jwt_token),
    # url(r'^api/v1/auth/refresh_token/', refresh_jwt_token),  
    # url(r'^api/v1/verify-token/', verify_jwt_token),  
]
