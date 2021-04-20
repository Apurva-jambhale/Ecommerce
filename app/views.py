from django.shortcuts import render, redirect
from django.views import View
from . models import Customer, Product, Cart, OrderPlaced
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages 
# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
    def get(self,request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        context = {
            'topwears' : topwears,
            'bottomwears' : bottomwears,
            'mobiles' : mobiles,
            'laptops' : laptops,
        }
        return render(request, 'app/home.html',context)


# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class ProductDetailView(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        context = {
            'product' : product
        }
        return render(request, 'app/productdetail.html',context)

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)

        amount = 0.0
        shipping_amount = 70.0
        for p in cart:
            tempamount =(p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
        totalitem = len(cart)

        context = {
            'carts' : cart,
            'totalamount' : totalamount,
            'amount' : amount,
            'totalitem' : totalitem
        }
        return render(request, 'app/addtocart.html',context)

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")
    #return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitem = len(Cart.objects.filter(user=request.user))
        context = {
            'form' : form,
            'totalitem' : totalitem,
            'active' : 'btn-primary'
        }
        return render(request, 'app/profile.html',context)
    
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congrulations. Profile Updated Successfully")
            totalitem = len(Cart.objects.filter(user=request.user))
            context = {
                'form' : form,
                'totalitem' : totalitem,
                'active' : 'btn-primary'
            }
            return render(request, 'app/profile.html',context)


def address(request):
    add = Customer.objects.filter(user=request.user)
    context = {
        'add':add,
        'active' : 'btn-primary'
    }
    return render(request, 'app/address.html',context)

def orders(request):
 return render(request, 'app/orders.html')

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request,data=None): 
    if data == None: 
        mobiles = Product.objects.filter(category='M')
    elif data == 'POCO' or data == 'SAMSUNG' or data == 'MOTOROLA': 
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below': 
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data == 'above': 
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    context = { 
        'mobiles':mobiles 
    } 
    return render(request, 'app/mobile.html',context) 

# def mobile(request,data=None):
#     if data == None:
#         mobiles = Products.objects.filter(category='M')
#     elif data == 'POCO' or data == 'MOTOROLA' or data == 'SAMSUNG':
#          mobiles = Products.objects.filter(category='M').filter(brand=data)
#     context = {
#         'mobiles' : mobiles
#     }
#     return render(request, 'app/mobile.html',context)

# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        context = {
            'form':form
        }
        return render(request, 'app/customerregistration.html',context)
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,"User Registered")
            form.save()
        context = {
            'form':form
        }
        return render(request, 'app/customerregistration.html',context)


def checkout(request):
 return render(request, 'app/checkout.html')


