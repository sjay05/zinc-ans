from django.db import models
from django.contrib.auth.models import User 
from mdeditor.fields import MDTextField

# extends django user
class ANSUser(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  is_enterprise = models.BooleanField(default=False, blank=True)
  enterprise_name = models.CharField(max_length=256, default="", blank=True)
  is_home_owner = models.BooleanField(default=False, blank=True)

  user_uid = models.CharField(max_length=256, blank=True, unique=True)
  address = models.CharField(max_length=256, default="", blank=True)

  trusted_enterprises = models.ManyToManyField(User, related_name = "trust_enterprise", blank=True)
  blocked_enterprises = models.ManyToManyField(User, related_name = "block_enterprise", blank=True)
  pending_enterprises = models.ManyToManyField(User, related_name = "pending_enterprise", blank=True) 

  def __str__(self):
    return self.user.username

class APIDocs(models.Model):
  content = MDTextField()



# Create your models here.
