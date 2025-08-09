from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from django.contrib import messages
from ..models import Blog,Likes,Comments

@login_required
def toggle_like(request,id):  
    BLOG= ContentType.objects.get_for_model(Blog)
    blog = Blog.objects.get(pk = id)
    likes = Likes.objects.filter(user=request.user,object_id = blog.pk ,content_type =  BLOG).exists()
    if not likes:
        Likes.objects.create(user = request.user,content_type = BLOG,content_object = blog)
    else :
        likes = Likes.objects.filter(user=request.user,content_type =  BLOG,object_id = blog.pk)
        likes.delete()

    return redirect(request.META.get("HTTP_REFERER", "/"))  # Fallback to homepage


@login_required
def set_comment(request,id):
    user_comment = request.POST.get("comment-field")
    print(user_comment)
    user = request.user
    blog = Blog.objects.get(pk = id)
    Comments.objects.create(comment = user_comment,user=user,blog=blog)

    return redirect(request.META.get("HTTP_REFERER"))
    

