from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class UserModel(AbstractUser):
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    otp = models.CharField(max_length=6)
    otp_send_time = models.DateTimeField(default=timezone.now)
    is_varified = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, default="")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def is_otp_valid(self, otp_entered):
        # Check if the entered OTP matches the stored OTP
        if self.otp == otp_entered:
            # Check if the OTP is expired (e.g., 5 minutes expiry duration)
            expiry_duration = datetime.timedelta(minutes=5)
            now = timezone.now()
            if now <= self.otp_send_time + expiry_duration:
                return True  # OTP is valid and not expired
        return False  # OTP is invalid or expired



# class Like(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'blog_post') 




class blogdata(models.Model):
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    blogimg = models.ImageField(upload_to="blog_app/static/images",default = "")
    blog_content = models.TextField(default='')
    publication_date = models.DateField(default=datetime.date.today)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, default= "")
    likes = models.ManyToManyField(UserModel, related_name='likes', blank=True)


    def __str__(self):
        return self.title



class Comment(models.Model):
    blog_post = models.ForeignKey(blogdata, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.created_at}'


