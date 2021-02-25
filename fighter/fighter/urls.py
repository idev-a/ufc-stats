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
from contest.views import (
    general_views,
    entry_views,
    event_views,
    user_views,
    chat_views,
    social_views,
    game_views
)
from rest_framework_extensions.routers import ExtendedSimpleRouter
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

router = ExtendedSimpleRouter()
event_router = router.register(r'events', event_views.EventViewSet)
event_router.register(
                r'bouts',
                general_views.BoutViewSet,
                basename='events-bout',
                parents_query_lookups=['event']
            )

router.register(r'^fighters', general_views.FighterViewSet)
router.register(r'^entries', entry_views.EntryViewSet)
router.register(r'^games', game_views.GameViewSet)
router.register(r'^users', user_views.UserViewSet)
router.register(r'^groups', general_views.GroupViewSet)

# chat
router.register(r'^chat/rooms', chat_views.ChatRoomViewSet)
router.register(r'^chat/rooms/(?P<id>\d+)$', chat_views.ChatRoomViewSet)
router.register(r'^chat/files', chat_views.ChatFileViewSet)
router.register(r'^chat/messages', chat_views.ChatMessageViewSet)
router.register(r'^chat/messages/(?P<id>\d+)$', chat_views.ChatMessageViewSet)

# customize admin
# class CustomAdminSite(admin.AdminSite):
  
#     def get_urls(self):
#         urls = super(CustomAdminSite, self).get_urls()
#         custom_urls = [
#             url(r'desired/path$', self.admin_view(organization_admin.preview), name="preview"),
#         ]
#         return urls + custom_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/registration/', include('rest_auth.registration.urls')),
    url(r'^auth/twitter/$', social_views.TwitterLogin.as_view(), name='twitter_login'),
    url(r'^auth/twitter/request_token/$', social_views.TwitterAuthRedirectEndpoint.as_view()),
    url(r'^auth/twitter/callback/$', social_views.TwitterCallbackEndpoint.as_view()),
    url(r'^auth/twitter/webhook/$', social_views.TwitterWebhookEndpoint.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
