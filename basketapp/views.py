from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from basketapp.models import Basket
from mainapp.models import Product

@login_required
def basket(request):
    content = {
        'basket': Basket.objects.filter(user=request.user)
    }
    return render(request, 'basketapp/basket.html', content)

@login_required
def basket_add(request, pk):    #pk = product_pk
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))
    product_item = get_object_or_404(Product, pk=pk)
    basket_item = Basket.get_product(user=request.user, product=product_item)
    # basket_item = Basket.objects.filter(product=product_item, user=request.user).first()
    if basket_item:
        # basket_item = Basket.objects.create(product=product_item, user=request.user)
        # basket_item = Basket(user=request.user, product=product_item)
        basket_item[0].quantity += 1
        basket_item[0].save()
    else:
        basket_item = Basket(user=request.user, product=product_item)
        basket_item.quantity += 1
        basket_item.save()

    # if not basket_item.exists():
    #     basket_item = Basket(user=request.user, product=product_item)

    # basket_item = basket_item[:0]
    #
    # basket_item.quantity += 1
    # basket_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_remove(request, pk):     #pk = basket_pk
    basket_item = get_object_or_404(Basket, pk=pk)
    basket_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_view(request):
    content = {}
    return render(request, 'basketapp/basket.html', content)

@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        print(f'{pk} - {quantity}')
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))
        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user)
        content = {
            'basket': basket_items,
        }
        result = render_to_string('basketapp/includes/inc_basket_list.html', content)
        return JsonResponse({'result': result})
