from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from .models import Product, Promotion, CatalogCategory, Catalog
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
    template_name = 'productions/view-product=edit-specification.html'
    paginate_by = 20
    ...


class ProductDetailView(DetailView):
    model = Product
    template_name = 'productions/product_detail.html'
    slug_field = 'code'  # new feature for me
    slug_url_kwarg = 'code'  # new feature for me


class ProductDeletionView(DeleteView):
    model = Product
    slug_field = 'code'
    slug_url_kwarg = 'code'


def product_delete(request, code):

    product = Product.objects.get(code=code)
    product.delete()
    return redirect('productions:product-list')


