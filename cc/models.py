from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Branch(models.Model):
    branch = models.TextField(default='')
    class Meta:
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'
    def __str__(self):
        return self.branch
    
class Category(models.Model):
    category = models.TextField(default='')
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.category

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    birth_date = models.DateField(null=True, blank=True)
    branch = models.ForeignKey("Branch", on_delete=models.CASCADE,default='')
    is_student = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.user.username

class Hod(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.ForeignKey("Branch", on_delete=models.CASCADE,default='')
    is_hod = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'HOD'
        verbose_name_plural = 'HODs'

    def __str__(self):
        return self.user.username

class Complaint(models.Model):
    complaint_details = models.TextField(default='')
    branch = models.ForeignKey("Branch", on_delete=models.CASCADE,related_name='compbranch')
    category = models.ForeignKey("Category", on_delete=models.CASCADE,related_name='compcategory')
    c_date = models.DateField(auto_now=True)
    class Status(models.TextChoices):
        PENDING = 'PN', _('Pending')
        SOLVED = 'SO', _('Solved')
        REJECTED = 'RJ',_('Rejected')
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PENDING,
    )
    owner = models.ForeignKey(User,null=True ,on_delete=models.SET_NULL,)
    class Meta:
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'

class Feedback(models.Model):
    comp_id = models.OneToOneField(Complaint,on_delete=models.CASCADE)
    feedback = models.TextField(default = '')
    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'