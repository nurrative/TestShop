from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Project",
        description="Boom Shaka Laka",
        default_version="v1",
    ),
    public=True
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.users.urls')),
    path('docs/', schema_view.with_ui("swagger")),
    path('api/', include('apps.products.urls')),
]
