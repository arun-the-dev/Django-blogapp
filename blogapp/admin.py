from django.contrib import admin
from .models import Category,Blog,Likes,Comments,User,Following
# Register your models here.
admin.site.register(Category)
admin.site.register(Blog)
admin.site.register(Likes)
admin.site.register(Comments)
admin.site.register(User)
admin.site.register(Following)