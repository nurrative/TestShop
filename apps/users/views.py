from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import RegisterUserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

class RegisterUserView(APIView):
    @swagger_auto_schema(request_body=RegisterUserSerializer())
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("User registered successfully.", status=201)


class CustomTokenRefreshView(TokenRefreshView):
   
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenObtainPairView(TokenObtainPairView):
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


