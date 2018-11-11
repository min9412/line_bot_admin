from django.db import models
from django.utils import timezone


# Create your models here.
class LineGroup(models.Model):
    id = models.AutoField(primary_key=True)
    line_group_id = models.CharField(max_length=100)
    # null=True 資料庫會把空格存成NULL
    # blank=True 從後台填寫表單時欄位可為空格
    line_group_name = models.CharField(max_length=100, null=True, blank=False)
    emba_group_name = models.CharField(max_length=100, null=True, blank=True)
    # get automatically
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=100, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=100, blank=True)


class AdminUser(models.Model):
    id = models.AutoField(primary_key=True)
    identity = models.CharField(max_length=100, null=True, blank=False)
    email = models.CharField(max_length=100, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=100, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=100, blank=True)
