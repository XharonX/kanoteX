from django.db import models
from django.db.models.signals import post_save, pre_save
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from employees.models import Employee, Technician, Sale
from productions.models import Product
from django.shortcuts import reverse
# from sale.models import OnlineSale
# Create your models here.


class FeeBy(models.TextChoices):
    comp = ('comp', 'company')
    cust = ('cust', 'customer')

class ServicingState(models.TextChoices):
    uncheck = 'nc', 'uncheck'
    serve = 's', 'servicing'
    check = 'c', 'checked'
    approve = 'y', 'approved'
    deny = 'n', 'deny'
    done = 'd', 'done'


class ErrorReturn(models.Model):
    STATUS = [
        ('delivering', 'deliver'),
        ('received', 'received'),
        ('checked', 'checked'),
        ('approved', 'approved'),
        ('done', 'done'),
    ]
    customer = models.CharField('customer name', max_length=255)
    # so_no = models.ForeignKey(OnlineSale, on_delete=models.SET_NULL, null=True, blank=True)
    so_no = models.CharField(_('Online Sale NO:'), max_length=20, blank=True, null=True)
    purchased_date = models.DateTimeField(auto_now_add=False, auto_created=False)
    purchased_shop = models.CharField('shop', max_length=100)
    product = models.ForeignKey(Product, max_length=30, on_delete=models.SET_NULL, null=True)
    qty = models.SmallIntegerField('qty')
    accessories = models.CharField(max_length=200)
    user_dmg = models.CharField('physical damage', max_length=255)
    reason = models.TextField()
    how = models.TextField(blank=True)
    received_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    received_at = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    # status = models.CharField(max_length=30, choices=ServicingState.choices, default='uncheck')

    def get_absolute_url(self):
        return reverse('services:finding', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.product) + " --> " + str(self.reason)


class Servicing(models.Model):
    technician = models.ForeignKey(Technician, on_delete=models.SET_NULL, null=True)
    form = models.OneToOneField(ErrorReturn, on_delete=models.CASCADE) # Error return form
    finding = models.TextField() # errors finding by technician
    checked = models.BooleanField(default=False) # is _ checked
    fnl_decision = models.CharField(max_length=250) # technician final decision
    fees = models.IntegerField(default=0)
    fees_by = models.CharField(_('fees_by'), max_length=40, choices=FeeBy.choices, default=FeeBy.comp)
    approved = models.BooleanField('approved', default=False, blank=True)
    done = models.BooleanField('approved', default=False, blank=True)

    def __str__(self):
        s = ""
        if self.checked:
            s = 'checked'
            if self.approved:
                s = 'approved'
                if self.done:
                    s = 'done'
        else:
            s = 'unchecked'

        p = f" Service Sr. {self.form.id}, {s} "

        return p


@receiver(post_save, sender=ErrorReturn)
def created_servicing(sender, instance, created, **kwargs):
    if created:
        Servicing.objects.create(form=instance)
    else:
        instance.servicing.form = instance
        instance.servicing.save()

