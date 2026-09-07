from django.urls import path, include

from loganalyzerapi import views

from django.conf import settings
from django.conf.urls.static import static

# Using Router
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()  #  automatically creates the API root view
router.register(r'logmaster', views.LogMasterViewSet)
router.register(r'logfile', views.LogFileViewSet)
router.register(r'loganalysisjob', views.LogAnalysisJobViewSet)
router.register(r'logdetail_v2', views.LogDetailV2ViewSet)

router.register(r'logdetail_dynamic', views.DynamicLogDetailViewSet, basename='logdetail_dynamic')


# For logformat
router.register(r'logformat', views.LogFormatViewSet)

router.register(r'logformatstring', views.LogFormatStringViewSet)

# For user
router.register(r'user', views.UserViewSet)

# For Metrics
router.register(r'metrics', views.MetricsViewSet)
router.register(r'logmastermetric', views.LogMasterMetricViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('mwla/', include(router.urls)),
    path('mwla/rest-auth/', include('dj_rest_auth.urls')),
    path(
        'mwla/rest-auth/registration/',
        include('dj_rest_auth.registration.urls'),
    )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 


#url(r'logdetail_test/<model>/', views.GeneralViewSet)
