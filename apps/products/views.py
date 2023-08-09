from rest_framework.generics import ListAPIView
from rest_framework.views import APIView 
from rest_framework.response import Response
import io
from rest_framework.permissions import IsAuthenticated
from openpyxl import Workbook
from django.http import HttpResponse
from .serializers import ProductSerializer
from .models import Product


class ProductListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=200)
    

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
