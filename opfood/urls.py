from django.contrib import admin
from django.urls import path,include
from opfood.views import api_root_view
from users import views
from debug_toolbar.toolbar import debug_toolbar_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Op Food Shop API",
      default_version='v1',
      description="API Documentation for Op Food Shop E-commarce Project.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root_view),
    path('api/', include('api.urls'), name='api-root'),
    path('activate/<uid>/<token>/', views.ActivateUser.as_view(), name='activate'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + debug_toolbar_urls()

