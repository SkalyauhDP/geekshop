from django.db import models

from basketapp.models import Basket
from geekshop import settings
from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUSES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PROCEEDED, 'обработано'),
        (PAID, 'оплачено'),
        (READY, 'готово к выдаче'),
        (CANCEL, 'отменено'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    status = models.CharField(max_length=3, choices=ORDER_STATUSES, default=FORMING, verbose_name='статус')
    is_active = models.BooleanField(default=True, verbose_name='активен')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания заказа')
    updated = models.DateTimeField(auto_now=True, verbose_name='дата обновления заказа')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return 'Текущий заказ: {}'.format(self.id)

    def get_total_quantity(self):
        _items = self.orderitems.select_related()
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity

    def get_product_type_quantity(self):
        items = self.orderitems.select_related()
        return len(items)

    def get_total_cost(self):
        _items = self.orderitems.select_related()
        _totalcost = sum(list(map(lambda x: x.quantity * x.product_cost, _items)))
        return _totalcost

    def delete(self):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='заказ', related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    quantity = models.PositiveIntegerField(default=0, verbose_name='количество')

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk)

