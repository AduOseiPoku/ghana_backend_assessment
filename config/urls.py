from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from schoolfees.views import SchoolViewSet, StudentViewSet, PaymentViewSet

router = DefaultRouter()
router.register('schools', SchoolViewSet, basename='school')
router.register('students', StudentViewSet, basename='student')
router.register('payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
