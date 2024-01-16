from django.shortcuts import render
from .models import ToDoList, ToDoItem
from django.views.generic import *


# Create your views here.

class ToDoListView(ListView):
    model = ToDoList
    template_name = 'reminder/todolist.html'


class ToDoSpecificView(DetailView):
    model = ToDoList
    template_name = 'reminder/specifictodo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['items'] = self.get_object.items
        return context


class ToDoItemSpecificView(DetailView):
    model = ToDoItem
    template_name = 'reminder/specifictodoitem.html'

