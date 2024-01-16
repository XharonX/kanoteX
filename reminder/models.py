from django.db import models
from employees.models import Employee
from django.template.defaultfilters import slugify
from django.shortcuts import reverse


# Create your models here.
class Purpose(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name


class ToDoList(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100)

    def get_absolute_url(self):
        return reverse('todo', self.slug)


class ToDoItem(models.Model):
    title = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    whatfor = models.ManyToManyField(Purpose)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=100, choices=ToDoStatus.choices, default='incomplete')
    priority = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    dead_line = models.DateTimeField(default=justaweek)

    def get_absolute_url(self):
        return reverse('todo-item', args=[str(self.title.slug), str(self.id)])

    def __str__(self):
        return f"{self.name}: {self.dead_line}"

    class Meta:
        ordering = ['priority', 'dead_line']
