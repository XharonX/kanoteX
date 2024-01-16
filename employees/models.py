from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.


class Employee(AbstractUser):
    email = models.EmailField(_('email'), max_length=255, unique=True)
    dept = models.ForeignKey('Department', related_name='dept', on_delete=models.SET_NULL, null=True)
    position = models.ForeignKey('Position', related_name='position', on_delete=models.SET_NULL, null=True)
    salary = models.IntegerField(_('salary'), blank=True, null=True, default=0)
    contact = models.CharField(_('phone'), max_length=12, blank=True, null=True)
    gender = models.CharField(_('gender'), max_length=10,
                              choices=(('male', 'male'), ('female', 'female'), ('none', 'none')), blank=True,
                              default='none', )
    age = models.IntegerField(_('age'), blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'employee'
        verbose_name_plural = 'employees'


class Position(models.Model):
    name = models.CharField(_('position'), max_length=100)

    def __str__(self):
        return self.name[:5].upper()


class Department(models.Model):
    name = models.CharField(_('department'), max_length=100)

    def __str__(self):
        return self.name[:4].upper()


class EmployeeManager(BaseUserManager):
    def __init__(self, dept):
        super().__init__()
        self.dept_id = dept

    def get_queryset(self, *args, **kwargs):
        member = super().get_queryset(*args, **kwargs)
        return member.filter(dept__id=self.dept_id)


class Technician(Employee):
    dept_id = 2
    objects = EmployeeManager(dept_id)

    def __str__(self):
        return f"{self.username}"

    class Meta:
        proxy = True
        verbose_name = 'Technician'


class Sale(Employee):
    dept_id = 1
    objects = EmployeeManager(dept_id)

    def __str__(self):
        return f"{self.username}"

    class Meta:
        proxy = True
        verbose_name = 'Sale'


class Others(Employee):
    dept_id = 1
    objects = EmployeeManager(dept_id)

    def __str__(self):
        return f"{self.username}"

    class Meta:
        proxy = True
        verbose_name = 'Others'


class DepartmentManager:
    def __init__(self):
        self._load_attribute()

    def _load_attribute(self):
        departments = Department.objects.all()
        for dept in departments:
            self.__setattr__(f'{dept.name[:4].upper()}', dept.id)


class PositionManager:
    def __init__(self):
        self._load_attribute()

    def _load_attribute(self):
        positions = Position.objects.all()
        for pos in positions:
            self.__setattr__(f'{pos.name[:5].upper()}', pos.id)
