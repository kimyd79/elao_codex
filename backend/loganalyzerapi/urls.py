from django.urls import path, include
from loganalyzerapi import views
from rest_framework.urlpatterns import format_suffix_patterns

from django.conf import settings
from django.conf.urls.static import static

# Using Router
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()  #  automatically creates the API root view
router.register(r'logmaster', views.LogMasterViewSet)
router.register(r'logfile', views.LogFileViewSet)
router.register(r'logdetail', views.LogDetailViewSet)

# For statistics 
router.register(r'logdetail/statistics_top1', views.LogDetailViewSet)
router.register(r'logdetail/statistics_top5', views.LogDetailViewSet)

# For chart
router.register(r'logdetail/chartdata', views.LogDetailViewSet)

# For logformat
router.register(r'logformat', views.LogFormatViewSet)
router.register(r'logformatstring', views.LogFormatStringViewSet)

# For user
router.register(r'user', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
