from django.shortcuts import redirect, render
from core.models import FoodCard, Category, ProductsCart
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def base(request):
    categories = Category.objects.all() 
    foodCards = FoodCard.objects.all()
    context = {'foodCards':foodCards, 'categories':categories}
    return render(request, 'index.html', context=context)


def addCart(request, pk):
    cart_session = request.session.get('cart_session', [])
    cart_session.append(pk)
    request.session['cart_session'] = cart_session
    return redirect('base')

def cart(request):
    cart_session = request.session.get('cart_session', [])
    count_of_product = len(cart_session)
    products_cart = FoodCard.objects.filter(id__in=cart_session)

    all_products_sum = 0
    for i in products_cart:
        i.count = cart_session.count(i.id)
        i.sum = i.count * i.price
        all_products_sum += i.sum

    return render(request, 'cart.html', {'products':products_cart,
                                         'count_of_product':count_of_product,
                                         'all_products_sum':all_products_sum} )


def removeCart(request, id):                        # 2
    cart = request.session.get('cart_session', [])  # 1, 2, 
    new_cart = []                                   # []
    for pk in cart:                                 
        if pk != id:                                # 1 != 2   2 != 2
            new_cart.append(pk)                     #   [1]    

    request.session['cart_session'] = new_cart      
    return redirect('cart')






# def test(request, id):
#     categories = Category.objects.all()
#     category = Category.objects.get(id=id)
#     # category1 = FoodCard.objects.all().filter(category=title)
#     print(categories)
#     return render(request, 'index.html', {'categories':categories, 'category':category})

def product(request, id):
    foodcard = FoodCard.objects.get(id=id)
    one_type_categories = FoodCard.objects.all().filter(category=foodcard.category)
    return render(request, 'product.html', {'foodcard':foodcard, 'one_type_categories':one_type_categories})




# def cart(request):
#     cart_session = request.session.get('cart_session', [])
#     count_of_product = len(cart_session)
#     products_Cart = FoodCard.objects.filter(id__in=cart_products)
#     all_products_sum = 0
#     for i in products_Cart:
#         i.count = cart_products.count(i.id)
#         i.sum = i.count * i.price
#         all_products_sum += i.sum
#         count_of_product += i.count
        
#     context = {
#         'products_Cart':products_Cart,
#         'all_products_sum':all_products_sum,
#         'count_of_product':count_of_product
#     }
#     return render(request, 'cart.html', context=context)


# cart_products = []
# res = {}
# def addCart(request, pk):
#     cart_session = request.session.get('cart_session', [])
#     cart_products.append(pk)
#     products_Cart = FoodCard.objects.filter(id__in=cart_products)
 
    # return HttpResponseRedirect('/')
    


# def removeCart(request, id):
#     cart_session = request.session.get('cart_session', [])
#     # cart = request.session.get('cart_session', []) # [1, 8]
#     new_cart = []
#     for fk in cart_session:
#         if fk != id:
#             new_cart.append(fk)

#     request.session['cart_session'] = new_cart
#     return redirect('cart')

def about(request):
    return render(request, 'about.html')


def search(request):
    if request.method == 'POST':
        searched_product = request.POST.get('search').title()
        # product = FoodCard.objects.get(name=searched_product)
        products = FoodCard.objects.filter(name__contains=searched_product)

        print(products)
        # print(product.price)
        print(searched_product)
    return render(request, 'search.html', {'searched_product':searched_product, 'products':products})


def signup(request):
    if request.method == 'POST':
        user = UserCreationForm(request.POST)
        if user.is_valid():
            user.save()
            return redirect('base')
    else:
        user = UserCreationForm()
    
    return render(request, 'auth.html', {'user':user})
    

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('base')
    else:
        form = AuthenticationForm()

    return render(request, 'auth.html', {'user':form})



def signout(request):
    logout(request)
    return redirect('base')


def order(request):
    return redirect('base')

    