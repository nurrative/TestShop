from django.urls import path
from .views import ProductListAPIView, ProductExportView

urlpatterns = [
    path('api/products/', ProductListAPIView.as_view()),
    path('api/products/export/', ProductExportView.as_view()),
]