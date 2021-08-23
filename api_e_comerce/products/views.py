from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Product

# Create your views here.


def ProductsView():
    template_name = 'products/list.html'
    context_object_name = 'product_list'

    def query_set(self):
        return Product.objects.order_by('name')