from rest_framework.generics import ListAPIView
from rest_framework.views import APIView 
from rest_framework.response import Response
import io
from rest_framework.permissions import IsAuthenticated
from openpyxl import Workbook
from django.http import HttpResponse
from .serializers import ProductSerializer
from .models import Product
from django.core.cache import cache
import redis
from django.conf import settings

# Подключение к Redis
redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


class ProductListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get_cached_products(self):
        cached_data = redis_client.get('cached_products')
        if cached_data:
            return cached_data
        else:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            serialized_data = serializer.data

            redis_client.setex('cached_products', 7200, serialized_data)

            return serialized_data

    def get(self, request, *args, **kwargs):
        cached_products = self.get_cached_products()
        return Response(cached_products, status=200)

    def invalidate_cache(self):
        redis_client.delete('cached_products')

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 201:
            self.invalidate_cache()

        return response

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)


        if response.status_code == 200:
            self.invalidate_cache()

        return response

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)

        if response.status_code == 204:
            self.invalidate_cache()

        return response
class ProductExportView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        wb = Workbook()
        ws = wb.active
        ws.title = "Products"

        headers = ["ID", "Name", "Description", "Category", "Price", "Created At", "Tags"]
        ws.append(headers)

        for product in serializer.data:
            tags = ', '.join(product["tags"])
            row_data = [product["id"], product["name"], product["description"], product["category_name"],
                        product["price"], product["created_at"], tags]
            ws.append(row_data)

        # Создание HTTP-ответа с содержимым Excel-файла
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=products.xlsx'
        output = io.BytesIO()
        wb.save(output)
        response.write(output.getvalue())

        return response
