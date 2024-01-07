from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save, pre_save
from django.shortcuts import reverse
# Create your models here.


class Brand(models.Model):
    name = models.CharField('name', max_length=100, )
    slug = models.SlugField(max_length=100)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    WARRANTY_MONTHS = [(m * 3, str(m * 3) + ' months') for m in range(1, 8)]
    code = models.CharField('code', max_length=20, unique=True, primary_key=True)
    name = models.CharField('product name', max_length=255, unique=True)
    # brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    # slug = models.SlugField('slug', blank=True, null=True)
    price = models.IntegerField('price')
    warranty = models.IntegerField('warranty', choices=WARRANTY_MONTHS)

    def get_absolute_url(self):
        return reverse('productions:product-detail', kwargs={'code': self.pk})

    # def save(self, *args, **kwargs):
    #     if self.slug is None:
    #         self.slug = slugify(self.name)
    #     return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} ({self.name})"


class Specification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='spec')
    label = models.CharField('Feature:', max_length=40)
    value = models.CharField('value', max_length=100)

    def __str__(self):
        return f"{self.product.code} + specifications"


# class Image(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, )
#     image = models.ImageField(upload_to='')
#     caption = models.CharField(max_length=100, blank=True, null=True)
#
#     def __str__(self):
#         return self.caption


class Catalog(models.Model):
    name = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(max_length=200, blank=True)
    publisher = models.CharField(max_length=300)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

    def __str__(self):
        return self.name


class CatalogCategory(models.Model):
    catalog = models.ForeignKey(Catalog, related_name='catalog', on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey('self', related_name='category', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    def __str__(self):
        if self.parent:
            return f"{self.catalog.name}:\t {self.parent.name} - {self.name}"
        return f"{self.catalog.name}:\t{self.name}"


class Promotion(models.Model):
    title = models.CharField(_('promotion event'), max_length=200, )
    items = models.ManyToManyField(Product)
    started_at = models.DateTimeField(auto_now_add=False, auto_created=False)
    end_at = models.DateTimeField(auto_now_add=False, auto_created=False)
    dis_percent = models.FloatField()
    discount = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        if self.discount == 0.0:
            total = sum(i.price for i in self.items.all())
            avg = total / self.items.count()
            self.discount = avg * (self.dis_percent / 100)
        return super().save(*args, **kwargs)


@receiver(post_save, sender=Product)
def create_specification_layout(sender, instance, created, *args, **kwargs):
    if created:
        Specification.objects.create(product=instance)
    else:
        instance.spec.form = instance
        instance.spec.save()
