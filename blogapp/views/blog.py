from django.shortcuts import render
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from django.db.models import Count
from django.urls import reverse_lazy
from  django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count,Exists,OuterRef
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..models import Blog,Category,Likes,Following,User
from ..forms.blog import BlogCreateForm,BlogUpdateForm
# Create your views here.
class BlogListView(ListView):
    model = Blog
    template_name="blog/blog-list.html"
    context_object_name = "blogs"
    paginate_by=10

    def get_queryset(self):
        search = self.request.GET.get("search")
        sort = self.request.GET.get("sort")
        category = self.request.GET.get("category")
        if search :  
            return Blog.objects.filter(title__icontains = search)
        final_query = Blog.objects
        if sort or category :
            if sort:
                if sort=="popular":
                    final_query = final_query.annotate(like_count = Count("likes")).order_by("-like_count")
                elif sort =="recent":
                    final_query =final_query.filter()
                elif sort =="title":
                    final_query = final_query.order_by("title")
            if category:
                return final_query.filter(category__pk = category)
            return final_query
        
        return Blog.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context
class BlogDetailView(DetailView):
    model = Blog
    template_name = "blog/blog-detail.html"
    context_object_name = "blog"

    def get_queryset(self):
        BLOG =  ContentType.objects.get_for_model(Blog)
        base_query = Blog.objects.prefetch_related("comments_set").select_related("author","category")
        if self.request.user.is_authenticated:
            user = self.request.user

            return base_query.annotate(
                like_count = Count("likes"),
                is_user_liked = Exists(Likes.objects.filter(content_type = BLOG,object_id=OuterRef("pk"),user = user)))
        return base_query.annotate(like_count = Count("likes"))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_blog = self.object
        similar_posts = Blog.objects.filter(category = current_blog.category).exclude(pk = current_blog.pk)[:10]
        context["similar_posts"] = similar_posts
        if self.request.user.is_authenticated:
            is_follower = Following.objects.filter(user = self.request.user,author = current_blog.author.pk).exists()
            context["is_follower"] = is_follower
        return context
class BlogCreateView(LoginRequiredMixin,CreateView):
    model = Blog
    form_class = BlogCreateForm
    template_name = "blog/blog-create.html"
    success_url = reverse_lazy("blog-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class BlogUpdateView(UpdateView):
    model = Blog
    form_class = BlogUpdateForm
    template_name = "blog/blog-update.html"
    success_url = reverse_lazy("blog-list")

    def form_valid(self, form):
        print(form.instance.main_pic)
        return super().form_valid(form)
    

class BlogDeleteView(DeleteView):
    model = Blog
    template_name = "blog/blog-delete.html"
    success_url = reverse_lazy("user-account")

# @login_required
def toggle_follow(request,author_id):
    try:
       user = request.user
       author = User.objects.get(pk = author_id)
       following = Following.objects.filter(user = user,author = author_id)
       if not following.exists():
            Following.objects.create(user = user,author = author)
            return JsonResponse({'status': 'followed'})
       else:
           following.delete()
           return JsonResponse({'status': 'unfollowed'})
    except:
       return JsonResponse({'error': 'Invalid request'}, status=400)