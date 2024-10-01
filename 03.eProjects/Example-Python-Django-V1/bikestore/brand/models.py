from django.db import models

# Create your models here.
class Brand(models.Model):
    class Meta:
        #Đổi tên table thành projectName_table_name
        db_table = 'bs_brands'
        #Sắp xếp mặc định
        ordering = ['brand_name']

        
    #Để hiện thị tên ở trong list Dashboard
    def __str__(self):
        return self.brand_name
    
    brand_name = models.CharField(max_length=50, unique=True) # Trường brand_name
    description = models.CharField(max_length=500, null=True,blank=True) # Trường description
    #created_at timestamp 
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    #created_at timestamp  
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # isActived BOOLEAN NOT NULL DEFAULT FALSE
    is_active = models.BooleanField(default=True)
