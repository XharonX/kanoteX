from django.shortcuts import render, redirect
from services.models import ErrorReturn, Servicing
from productions.models import Product
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.views.generic import View, CreateView, TemplateView, FormView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login
from .models import Employee
from .forms import *
from django.urls import reverse_lazy
# Create your views here.


class EmployeeLoginView(FormView):
    template_name = 'auth/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('desktop')

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, self.template_name, {
                'form': self.form_class
            })
        else:
            return HttpResponseForbidden(
                '<h1> 405 You are allowed this page. </h1>'
            )
    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            username = request.POST.get('username')
            password = request.POST.get('password')
            account = authenticate(request, username=username, password=password)
            if account is not None:
                login(request, account)
                return redirect(self.success_url)
            else:
                messages.error(request, 'Failed Authenticated')
                return redirect(request.META.get("HTTP_REFERER"))
        else:
            return redirect('desktop')


class EmployeeCreationView(CreateView):
    template_name = 'auth/register.html'
    form_class = EmployeeCreationForm
    success_url = reverse_lazy('desktop')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            fst = form.cleaned_data['first_name']
            lst = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            dept = form.cleaned_data['dept']
            pos = form.cleaned_data['position']
            salary = form.cleaned_data['salary']
            contact = form.cleaned_data['contact']
            gender = form.cleaned_data['gender']
            age = form.cleaned_data['age']
            password = form.cleaned_data['password']

            try:
                emp = Employee(first_name=fst, last_name=lst, username= username, email=email,\
                               dept=dept, position=pos, is_staff= True, salary=salary,\
                               contact=contact, gender=gender,  age=age)
                emp.set_password(password)
                emp.save()
                return redirect('desktop')
            except ValueError:
                return "Cannot Create an employee staff."


class DashboardView(TemplateView):
    model = Employee
    template_name = 'employees/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['error_return'] = ErrorReturn.objects.all()
        context['servicing'] = Servicing.objects.all()
        context['products'] = Product.objects.all()

        return context


class EmployeeLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        reverse_lazy('login')
