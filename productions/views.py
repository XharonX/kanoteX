from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from .models import Product, Promotion, CatalogCategory, Catalog
from django.db.models import Q
import pandas as pd
# Create your views here.


class ProductCreationView(CreateView):
    form_class = ProductCreationForm
    template_name = 'productions/create_edit_products.html'
    success_url = 'productions:product-list'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"{form.cleaned_data['name']} has been created.")
        return redirect(self.success_url)


class ProductListView(ListView):
    model = Product
    template_name = 'productions/product_list.html'
    paginate_by = 20

    def get_queryset(self):
        qs = self.request.GET.get('q', '')
        rst = self.model.objects.filter(Q(name__icontains=qs) | Q(code__icontains=qs))
        return rst

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return render(request, self.template_name, {'object_list': self.object_list})


class ProductDetailView(DetailView):
    model = Product
    template_name = 'productions/product_detail.html'
    slug_field = 'code'  # new feature for me
    slug_url_kwarg = 'code'  # new feature for me

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        obj.errorreturn_set.all()
        context['product'] = obj
        context['error_return'] = obj.errorreturn_set.all()
        context['label'] = 0
        return context


class ProductDeletionView(DeleteView):
    model = Product
    slug_field = 'code'
    slug_url_kwarg = 'code'


def product_delete(request, code):

    product = Product.objects.get(code=code)
    product.delete()
    return redirect('productions:product-list')


class BrandCreationView(CreateView):
    model = Brand
    template_name = 'productions/create-brand.html'
    success_url = 'productions:product-list'
    form_class = BrandCreationForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_product')


