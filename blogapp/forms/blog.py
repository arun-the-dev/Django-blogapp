from django.forms import ModelForm


from ..models import Blog



class BlogCreateForm(ModelForm):
    class Meta:
        model = Blog
        fields = ["title","main_pic","content","category"]

class BlogUpdateForm(ModelForm):
    class Meta:
        model = Blog
        fields = ["title","main_pic","content","category"]