from itertools import product
from re import A
from django.shortcuts import render, redirect
from django.views import View

from app.forms import CustomerProfileForm, CustomerRegistrationForm
from . models import Customer, Product, OrderPlaced, Cart
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from rest_framework.decorators import api_view
from rest_framework.response import Response



class ProductView(View):
    def get (self, request):
        totalitem = 0
        topwears = Product.objects.filter(category='Top Wear')
        bottomwears = Product.objects.filter(category='Bottom Wear')
        mobiles = Product.objects.filter(category='Mobile')
        #laptops = Product.objects.filter(category='Laptop')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render (request, 'app/home.html', {'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles, 'totalitem':totalitem})


class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        
        return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart,  'totalitem':totalitem})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        #print(cart)
        amount = 0.0
        shipping_amount = 50.0
        total_aamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        #print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price )
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount, 'totalitem':totalitem})

        else:
            return render(request, 'app/emptycart.html')


        
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 50.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price )
            amount += tempamount
          
            data = {
                'quantity': c.quantity,
                'amount':amount,
                'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)    

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 50.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price )
            amount += tempamount
          
            data = {
                'quantity': c.quantity,
                'amount':amount,
                'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        
        c.delete()
        amount = 0.0
        shipping_amount = 50.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price )
            amount += tempamount
          
        data = {
            'amount':amount,
            'totalamount':amount + shipping_amount
        }
        return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'} )

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully')

        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add, 'active':'btn-primary '})

@login_required
def orders(request):
    orders = OrderPlaced.objects.filter(user=request.user)

    return render(request, 'app/orders.html', {'orders':orders})


def mobile(request,  data=None):
    if data == None:
        mobiles = Product.objects.filter(category='Mobile')
    elif data == 'RedMi' or data == 'Samsung' or data == 'OnePlus' or data == 'Motorala' or data == 'Realme' or data == 'Vivo':
        mobiles = Product.objects.filter(category='Mobile').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='Mobile').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='Mobile').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html', {'mobiles':mobiles})

def laptop(request,  data=None):
    if data == None:
        laptops = Product.objects.filter(category='Laptop')
    return render(request, 'app/laptop.html', {'laptops':laptops})



def topwear(request, data=None):
    if data == None:
        topwears = Product.objects.filter(category='Top Wear')
    elif data == 'below':
        topwears = Product.objects.filter(category='Top Wear').filter(discounted_price__lt=250)
    elif data == 'above':
        topwears = Product.objects.filter(category='Top Wear').filter(discounted_price__gt=250)
    return render(request, 'app/topwear.html', {'topwears':topwears})

def bottomwear(request, data=None):
    if data == None:
        bottomwears = Product.objects.filter(category='Bottom Wear')
    elif data == 'below':
        bottomwears = Product.objects.filter(category='Bottom Wear').filter(discounted_price__lt=450)
    elif data == 'above':
        bottomwears = Product.objects.filter(category='Bottom Wear').filter(discounted_price__gt=450)
    return render(request, 'app/bottomwear.html', {'bottomwears':bottomwears})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registred Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 50.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price )
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items})

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

