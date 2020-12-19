"""Create users for Selenum tests"""
from django.contrib.auth.models import User


user = User.objects.create_user('walrus', password='wal')
user.is_superuser = True
user.is_staff = True
user.save()
user = User.objects.create_user('chifir', password='thispasswordistooshort')
user.save()
