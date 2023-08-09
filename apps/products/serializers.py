from rest_framework import serializers
from .models import *


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name',)


class ProductSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'category_name', 'price', 'created_at', 'tags')

    def get_category_name(self,obj):
        return obj.category_id.name
    
    def get_tags(self, obj):
        return obj.tags.values_list('name', flat=True)
    


    


