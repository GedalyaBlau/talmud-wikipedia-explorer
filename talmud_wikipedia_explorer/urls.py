from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('explorer.urls')),
    path('accounts/', include('allauth.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
]
