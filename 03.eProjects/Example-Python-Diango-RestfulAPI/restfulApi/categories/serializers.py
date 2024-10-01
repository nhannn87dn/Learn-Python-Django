# myapp/serializers.py
from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    #Validate cơ bản
    name = serializers.CharField(max_length=100, allow_blank=False)
    #Validate custom
    def validate_name(self, value):
        # Thực hiện kiểm tra logic tùy ý
        if len(value) < 3:
            raise serializers.ValidationError("Tên phải có ít nhất 3 ký tự.")
        return value
    
    class Meta:
        #Tên Model sử dụng
        model = Category
        #Hiển thị tất cả các trường
        fields = '__all__'
  