from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from .user import User
from ckeditor.fields import RichTextField
# from django.utils.timesince import timesince

from ..helpers import calculate_time_ago




# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.category


class Blog(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    main_pic = models.ImageField(upload_to="main_pics/",default="defaults/blog_main_pic_default.png")
    content = RichTextField()
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = GenericRelation('Likes') 
    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author} blog - {self.title[0:10]}.."

    
    def time_posted_ago(self):
        return calculate_time_ago(self.created_at)
    
    def author_full_name(self):
        return self.author.first_name + " " + self.author.last_name
    def like_count(self):
        return self.likes.count()
    

class Comments(models.Model):
    comment = models.TextField()
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        ordering = ["-created_at"]
    def __str__(self):
        return f"{self.comment} - {self.user.get_full_name}"
        
    def time_posted_ago(self):      
        return calculate_time_ago(self.created_at)
class Likes(models.Model):
    # type of the model is stored here
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    # referencing the pk id of original model like Blog id=5 
    object_id = models.PositiveIntegerField()
    # it directly reteives the object instance of the model
    content_object = GenericForeignKey("content_type","object_id")
    # blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        #user likes a blog one time 
        # unique_together = ('user',"blog")
        unique_together = ('user',"content_type",'object_id')
        # modern method to unique
        #     constraints = [
        #     UniqueConstraint(fields=['user', 'content_type', 'object_id'], name='unique_comment_per_user_per_object')
        # ]

    def __str__(self):
        return f"liked by {self.user.get_full_name}"
    
class Following(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author_set')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} following {self.author.first_name}"
    
    class Meta:
        unique_together = ('user','author')