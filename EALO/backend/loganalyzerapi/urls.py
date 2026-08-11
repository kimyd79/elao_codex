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

# For Ceating Dynamic Logdetail
router.register(r'logmaster/create_dynamic_logdetail', views.LogMasterViewSet)
router.register(r'logmaster/delete_dynamic_logdetail', views.LogMasterViewSet)
router.register(r'logdetail_dynamic', views.DynamicLogDetailViewSet, basename='logdetail_dynamic')
router.register(r'logdetail_dynamic/start_end', views.DynamicLogDetailViewSet, basename='logdetail_dynamic')
router.register(r'logdetail_dynamic/notice', views.DynamicLogDetailViewSet, basename='logdetail_dynamic')
router.register(r'logdetail_dynamic/statistics', views.DynamicLogDetailViewSet, basename='logdetail_dynamic')
router.register(r'logdetail_dynamic/chartdata', views.DynamicLogDetailViewSet, basename='logdetail_dynamic')
router.register(r'logdetail_dynamic/findings', views.DynamicLogDetailViewSet, basename='logdetail_dynamic')
router.register(r'logdetail_dynamic/get_before_after_detail', views.DynamicLogDetailViewSet, basename='logdetail_dynamic')
router.register(r'logdetail_dynamic/chartdata_diff', views.DynamicLogDetailViewSet, basename='logdetail_dynamic')

router.register(r'logdetail_dynamic/uridetail', views.DynamicLogDetailViewSet, basename='logdetail_dynamic')


# For logformat
router.register(r'logformat', views.LogFormatViewSet)
router.register(r'logformat/assist', views.LogFormatViewSet)

router.register(r'logformatstring', views.LogFormatStringViewSet)
router.register(r'logformatstring/formatkind_list', views.LogFormatStringViewSet, basename='logformatstring')

# For user
router.register(r'user', views.UserViewSet)
router.register(r'user/active', views.UserViewSet)

# For Metrics
router.register(r'metrics', views.MetricsViewSet)
router.register(r'logmastermetric', views.LogMasterMetricViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('mwla/', include(router.urls)),
    path('mwla/rest-auth/', include('rest_auth.urls')),
    path('mwla/rest-auth/registration/', include('rest_auth.registration.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 


#url(r'logdetail_test/<model>/', views.GeneralViewSet)