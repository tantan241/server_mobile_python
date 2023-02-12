from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission,User
# Create your models here.
# class CustomUser(User):
#     # idGoogle =models.CharField(max_length=50,unique=True)
#     # username =models.CharField(max_length=50,default="",null=True,blank=True)
#     # # password =models.CharField(max_length=50,default="")
#     # email =models.EmailField(max_length=50,default="")
#     # # phoneNumber =models.CharField(max_length=16,default="")
#     # fullName =models.CharField(max_length=50,default="")
#     # status=models.IntegerField(default=0,null=True,blank=True)
#     # USERNAME_FIELD = 'idGoogle'
#     # REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
#     # username =models.CharField(max_length=50,default="",null=True,blank=True)
#     # groups = models.ManyToManyField(
#     #     Group,
#     #     related_name='custom_user_groups',
#     #     blank=True,
#     #     help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
#     #     related_query_name='custom_user',
#     # )
#     # user_permissions = models.ManyToManyField(
#     #     Permission,
#     #     related_name='custom_user_permissions',
#     #     blank=True,
#     #     help_text='Specific permissions for this user.',
#     #     related_query_name='custom_user',
#     # )
#         class Meta:
#             app_label = 'user'
#             verbose_name = 'User'
#             verbose_name_plural = 'Users'
            
#         fullName =models.CharField(max_length=50,default="")
class CustomUser(User):
    fullName = models.CharField(max_length=100)
    # email = models.EmailField(max_length=100, unique=True)
    def __str__(self):
        return self.fullName
            
        
