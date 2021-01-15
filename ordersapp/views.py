# from django.shortcuts import render
from django.views.generic import ListView

from ordersapp.models import Order


class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        # queryset = super().get_queryset()
        return Order.objects.filter(user=self.request.user)
