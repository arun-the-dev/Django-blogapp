from django.urls import path



from .views.blog import BlogListView,BlogCreateView,BlogUpdateView,BlogDeleteView,BlogDetailView,toggle_follow
from .views.likes_comments import toggle_like,set_comment

urlpatterns = [
    path("",BlogListView.as_view(),name="blog-list"),
    path("create/",BlogCreateView.as_view(),name="blog-create"),
    path("update/<int:pk>/",BlogUpdateView.as_view(),name="blog-update"),
    path("delete/<int:pk>/",BlogDeleteView.as_view(),name="blog-delete"),
    path("detail/<int:pk>/",BlogDetailView.as_view(),name="blog-detail"),
    path("blog/<int:id>/like/",toggle_like,name="blog-like"),
    path("blog/<int:id>/comment/",set_comment,name="blog-comment"),
    path("follow/author/<int:author_id>",toggle_follow,name = "toggle-follow")
]