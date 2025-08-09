from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from datetime import timedelta
import uuid

from ..forms.auth import LoginForm
from ..models import User,Blog,Otp,Likes,Following
from ..helpers import generate_random_otp
from ..tasks import send_otp_email
from .. import constants
def user_login(request):
    # print(request.user)
    # if request.user is not None:
    #     return redirect("blog-list")
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        # email = request.POST.get("email_field")
        # password = request.POST.get("password_field")

        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        print(email,password)
        user = authenticate(request,email=email, password = password)
        print(user)
        if user is not None:
            login(request,user)
            return redirect("blog-list")
        else:
            form.add_error(None, "Invalid email or password")
    return render(request,"auth/login.html",{"form":form})

def user_register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name_field")
        last_name = request.POST.get("last_name_field")
        email = request.POST.get("email_field")
        password = request.POST.get("password_field")
        profile_pic = request.FILES.get("profile_pic_field")
        user = User.objects.filter(email = email).exists()
        if not user:             
            user = User.objects.create_user(email=email,password=password,first_name=first_name,last_name=last_name,profile_pic=profile_pic)
            return redirect("login")
        messages.error(request,"Email is aldready Registered")
        return render(request,"auth/register.html")
    return render(request,"auth/register.html")

def user_update(request):
    user = User.objects.filter(pk=request.user.pk)
    if request.method == "POST" and user:
        first_name = request.POST.get("first_name_field")
        last_name = request.POST.get("last_name_field")
        email = request.POST.get("email_field")
        profile_pic = request.FILES.get("profile_pic_field","")
        temp={}
        if first_name:
            temp["first_name"] = first_name
        if last_name:
            temp["last_name"] = last_name
        if email:
            temp["email"] = email
        if profile_pic:
            temp["profile_pic"] = profile_pic

        user.update(**temp)
        messages.success(request,"Update Successfull")
        return redirect("user-account")
    return render(request,"auth/update.html",{"user":user.first()})

@login_required
def user_account(request):
        BLOG = ContentType.objects.get_for_model(Blog)
        query = request.GET.get("q")
        if query == None:
            blogs = Blog.objects.filter(author = request.user)
            return render(request,"auth/account.html",{"blogs":blogs})
        elif query == "user-like-blogs":
            user_liked_blogs = Likes.objects.filter(content_type = BLOG).filter(user = request.user)
            return render(request,"auth/account.html",{"user_liked_blogs":user_liked_blogs})
        else :
            following = Following.objects.filter(user = request.user)
            print(following)
            return render(request,"auth/account.html",{"user_following_authors":following})

        

def user_forget_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email)

        if user.exists():
            otp = generate_random_otp()

            # Save OTP with expiry and send
            otp_obj = Otp.objects.create(
                user=user.first(),
                code=otp,
                expires_at=timezone.now() + timedelta(minutes=10),
                is_used=False
            )
            send_otp_email.delay(email, otp)

            # Store in session
            request.session["otp_id"] = str(otp_obj.id)
            request.session["otp_email"] = email

            return redirect(reverse("verify-otp"))

        else:
            messages.error(request, "No user with this email.")
            return render(request, "auth/forget-password.html")

    return render(request, "auth/forget-password.html")

def verify_otp(request):
    otp_id = request.session.get("otp_id")
    email = request.session.get("otp_email")

    if not (otp_id and email):
        return HttpResponse("Unauthorized")

    if request.method == "POST":
        entered_otp = request.POST.get("otp")

        try:
            otp_obj = Otp.objects.get(
                id=uuid.UUID(otp_id),
                code=entered_otp,
                is_used=False
            )

            if otp_obj.expires_at < timezone.now():
                messages.error(request, "OTP has expired.")
            else:
                otp_obj.is_used = True
                otp_obj.save()
                return redirect("reset-password")

        except Otp.DoesNotExist:
            messages.error(request, "Invalid OTP.")

    return render(request, "auth/verify-otp.html", {"otp_sent": True, "email": email})


def reset_password(request):
    otp_id = request.session.get("otp_id")

    if request.method == "POST":
        if not otp_id:
            return HttpResponse("Session expired. Please try again.")

        try:
            otp_obj = Otp.objects.get(id=uuid.UUID(otp_id))
            user = otp_obj.user
            password = request.POST.get("password")

            if not password:
                return HttpResponse("Password cannot be empty.")

            user.set_password(password)
            user.save()

            otp_obj.delete()
            request.session.pop("otp_id", None)
            request.session.pop("otp_email", None)
            messages.success(request,"Password reset successfull")
            return redirect("login")

        except Otp.DoesNotExist:
            return HttpResponse("Invalid or expired OTP.")

    if otp_id:
        return render(request, "auth/password-reset.html")
    else:
        return HttpResponse("Unauthorized access.")
def author_account(request,author_id):
    query = request.GET.get("q")
    author = User.objects\
    .annotate(followers_count = Count('author_set',distinct=True),blog_count = Count('blog'))
    if query == None:
        author = author.prefetch_related('blog_set').get(pk = author_id)
        return render(request,"auth/author-account.html",{
            "author":author
        })
    else:
        author = author.get(pk = author_id)
        author_followers = author.author_set.all()
        return render(request,"auth/author-account.html",{
            "author":author,
            "author_followers":author_followers
        })
