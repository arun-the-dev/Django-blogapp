from django.db.models.signals import pre_save,post_delete
from django.dispatch import receiver
import os
from .models import Blog
@receiver(pre_save,sender=Blog)
def delete_old_image_if_blog_updated(sender,instance,**kwargs):
    
    if not instance.pk:
        return 
    try :
       old_blog =  Blog.objects.get(pk = instance.pk)
    except Blog.DoesNotExist:
        return 
    old_image = old_blog.main_pic
    new_image = instance.main_pic
    print(old_image,new_image)
    if old_image and old_image != new_image:
        print(True)
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)

@receiver(post_delete,sender = Blog)
def delete_blog_image_if_blog_deleted(sender,instance,**kwargs):
    if instance.main_pic:
        image_path = instance.main_pic.path
        if os.path.isfile(image_path):
            os.remove(image_path)