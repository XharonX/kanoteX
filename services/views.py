from django.shortcuts import render, redirect
from employees.models import Employee
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from productions.models import Product
from .models import Servicing, ErrorReturn
from django.db.models import Q
from django.http.response import JsonResponse, HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.urls import reverse_lazy
from .forms import ServiceForm, TechFindingForm
from employees.models import DepartmentManager, PositionManager
import pandas as pd
# Create your views here.

dept = DepartmentManager()
pos = PositionManager()


class CreateServiceForm(CreateView):
    form_class = ServiceForm
    template_name = 'service-dept/received_service.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = request.user
            print(user)
            if request.user.is_authenticated and request.user.dept_id == dept.SALE:
                received_by = Employee.objects.get(username=user.username)
                instance = form.save(commit=False)
                instance.received_by = received_by
                instance.save()
                messages.success(request, _(f"Error Service has been created {request.user}"))
                return redirect('services:error_list')
            else:
                messages.error(request, form.errors)
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, form.errors)
            return redirect(request.META.get('HTTP_REFERER'))


class EditServiceForm(UpdateView):
    model = ErrorReturn
    template_name = 'service-dept/received_service.html'
    form_class = ServiceForm
    success_url = reverse_lazy('services:error_list')

    def get_object(self, queryset=None):
        return ErrorReturn.objects.get(pk=self.kwargs['pk'])


class DeleteServiceForm(DeleteView):
    model = ErrorReturn
    success_url = reverse_lazy('services:error_list')


class ReturnErrorListView(ListView):
    model = ErrorReturn
    template_name = 'service-dept/return_error_list.html'
    ordering = ['-received_at']
    paginate_by = 20

    def get_queryset(self):
        qs = self.request.GET.get('q', '')
        print(qs)
        if qs == 'all':
            result = self.model.objects.all()
        else:
            result = self.model.objects.filter(Q(customer__icontains=qs) | Q(purchased_shop__icontains=qs))
        return result

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return render(request, self.template_name, {'object_list': self.object_list})

class FindingResultView(UpdateView):
    form_class = TechFindingForm
    model = Servicing
    template_name = 'service-dept/finding_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['received_form'] = self.object.form
        return context

    def post(self, request, *args, **kwargs):
        tech_form = self.form_class(request.POST)
        instance = self.get_object().form
        if request.user.is_authenticated:
            technician = request.user
        if tech_form.is_valid():
            try:
                servicing = instance.servicing

                if servicing.checked:
                    servicing.approved = True
                    servicing.form.status = 'approved'

                else:
                    servicing.technician = technician
                    servicing.finding = tech_form.cleaned_data['finding']
                    servicing.fnl_decision = tech_form.cleaned_data['fnl_decision']
                    servicing.fees = tech_form.cleaned_data['fees']
                    servicing.fees_by = tech_form.cleaned_data['fees_by']
                    if len(servicing.fnl_decision) > 5:
                        servicing.checked = True
                        instance.status = 'checked'
                servicing.save()
                instance.save()
                messages.success(request, _("Finished finding. Ready to return back  to customer or shop"))
                return redirect('services:error_list')
            except ErrorReturn.DoesNotExist() or Servicing.DoesNotExist():
                return HttpResponse("Invalid Service Finding for the Service Form")
        else:
            print(tech_form.errors)
            messages.error(request, tech_form.errors)
            return redirect(request.META.get("HTTP_REFERER"))


class ErrorApprovingView(UpdateView):
    form_class = TechFindingForm
    model = Servicing
    template_name = 'service-dept/finding_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['received_form'] = self.object.form
        return context

    def post(self, request, *args, **kwargs):
        tech_form = self.form_class(request.POST)
        instance = self.get_object().form
        if request.user.is_authenticated:
            technician = request.user
        if tech_form.is_valid():
            try:
                servicing_instance = instance.servicing
                servicing_instance.technician = technician
                servicing_instance.finding = tech_form.cleaned_date['finding']
                servicing_instance.f_decision = tech_form.cleaned_date['f_decision']
                servicing_instance.fees = tech_form.cleaned_date['fees']
                servicing_instance.fees_by = tech_form.cleaned_date['fees_by']
                if servicing_instance.checked == True:
                    servicing_instance.approved = True
                servicing_instance.save()
                messages.success(request, _("Finished finding. Ready to return back  to customer or shop"))
                return redirect('services:error_list')
            except ErrorReturn.DoesNotExist() or Servicing.DoesNotExist():
                return HttpResponse("Invalid Service Finding for the Service Form")
        else:
            messages.error(request, tech_form.errors)
            return redirect(request.META.get("HTTP_REFERER"))


def get_product_info(request, product):
    try:
        product = Product.objects.get(code=product)
        data = {
            'name': product.name,
            'code': product.code,
        }
        return JsonResponse(data)
    except Product.DoesNotExist():
        return JsonResponse(
            {
                'error': 'Product NOT Found',
            }, status=404
        )


def get_warranty_rule(request):
    return render(request, 'service-dept/warranty_rules.html')


def analysis_error_return():
    df = ErrorReturn.objects.all()
    c_list = df['product_id'].value_counts()


