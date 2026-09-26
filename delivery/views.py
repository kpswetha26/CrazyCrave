
import razorpay
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Cart, Customer, Item, Restaurant

# =========================================================
# HOME
# =========================================================

def index(request):
    return render(
        request,
        'delivery/index.html'
    )


# =========================================================
# ADMIN HOME
# =========================================================

def admin_home(request):
    return render(
        request,
        'delivery/admin_home.html'
    )


# =========================================================
# CUSTOMER HOME
# =========================================================

def customer_home(request, username):

    restaurantList = Restaurant.objects.all()

    return render(
        request,
        'delivery/customer_home.html',
        {
            'restaurantList': restaurantList,
            'username': username
        }
    )


# =========================================================
# SIGN UP
# =========================================================

def open_signup(request):

    return render(
        request,
        'delivery/signup.html'
    )


def signup(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        # Check duplicate username
        if Customer.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                'delivery/signup.html',
                {
                    'error':
                    'Username already exists. Please choose another username.'
                }
            )

        # Create customer
        Customer.objects.create(
            username=username,
            password=password,
            email=email,
            mobile=mobile,
            address=address
        )

        # Go to signin page
        return render(
            request,
            'delivery/signin.html',
            {
                'success':
                'Account created successfully! Please sign in.'
            }
        )

    return render(
        request,
        'delivery/signup.html'
    )


# =========================================================
# SIGN IN
# =========================================================

def open_signin(request):

    return render(
        request,
        'delivery/signin.html'
    )


def signin(request):

    # If user directly opens /signin/user/
    if request.method == 'GET':

        return render(
            request,
            'delivery/signin.html'
        )

    # Get login values
    username = request.POST.get('username')
    password = request.POST.get('password')

    print("USERNAME:", username)
    print("PASSWORD:", password)

    # Check username and password
    customer = Customer.objects.filter(
        username=username,
        password=password
    ).first()

    # Login failed
    if customer is None:

        print("LOGIN FAILED")

        return render(
            request,
            'delivery/signin.html',
            {
                'error':
                'Invalid username or password.'
            }
        )

    # Login successful
    print(
        "LOGIN SUCCESS:",
        customer.username
    )

    # Admin
    if username == 'admin':

        return redirect(
            'admin_home'
        )

    # Normal customer
    return redirect(
        'customer_home',
        username=username
    )


# =========================================================
# ADD RESTAURANT
# =========================================================

def open_add_restaurant(request):

    return render(
        request,
        'delivery/add_restaurant.html'
    )


def add_restaurant(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')

        # Check duplicate restaurant
        if Restaurant.objects.filter(
            name=name
        ).exists():

            return HttpResponse(
                "Duplicate restaurant!"
            )

        Restaurant.objects.create(
            name=name,
            picture=picture,
            cuisine=cuisine,
            rating=rating
        )

        return redirect(
            'open_show_restaurant'
        )

    return redirect(
        'open_add_restaurant'
    )


# =========================================================
# SHOW RESTAURANTS
# =========================================================

def open_show_restaurant(request):

    restaurantList = Restaurant.objects.all()

    return render(
        request,
        'delivery/show_restaurant.html',
        {
            'restaurantList':
            restaurantList
        }
    )


# =========================================================
# UPDATE RESTAURANT
# =========================================================

def open_update_restaurant(
    request,
    restaurant_id
):

    restaurant = get_object_or_404(
        Restaurant,
        id=restaurant_id
    )

    return render(
        request,
        'delivery/update_restaurant.html',
        {
            'restaurant':
            restaurant
        }
    )


def update_restaurant(
    request,
    restaurant_id
):

    restaurant = get_object_or_404(
        Restaurant,
        id=restaurant_id
    )

    if request.method == 'POST':

        restaurant.name = request.POST.get(
            'name'
        )

        restaurant.picture = request.POST.get(
            'picture'
        )

        restaurant.cuisine = request.POST.get(
            'cuisine'
        )

        restaurant.rating = request.POST.get(
            'rating'
        )

        restaurant.save()

        return redirect(
            'open_show_restaurant'
        )

    return redirect(
        'open_update_restaurant',
        restaurant_id=restaurant_id
    )


# =========================================================
# DELETE RESTAURANT
# =========================================================

def delete_restaurant(
    request,
    restaurant_id
):

    restaurant = get_object_or_404(
        Restaurant,
        id=restaurant_id
    )

    restaurant.delete()

    return redirect(
        'open_show_restaurant'
    )


# =========================================================
# MANAGE MENU
# =========================================================

def open_update_menu(
    request,
    restaurant_id
):

    restaurant = get_object_or_404(
        Restaurant,
        id=restaurant_id
    )

    itemList = restaurant.items.all()

    return render(
        request,
        'delivery/update_menu.html',
        {
            'itemList': itemList,
            'restaurant': restaurant
        }
    )


# =========================================================
# ADD FOOD ITEM
# =========================================================

def update_menu(
    request,
    restaurant_id
):

    restaurant = get_object_or_404(
        Restaurant,
        id=restaurant_id
    )

    if request.method == 'POST':

        name = request.POST.get(
            'name'
        )

        description = request.POST.get(
            'description'
        )

        price = request.POST.get(
            'price'
        )

        vegeterian = (
            request.POST.get('vegeterian')
            == 'on'
        )

        picture = request.POST.get(
            'picture'
        )

        # Check duplicate item
        if Item.objects.filter(
            restaurant=restaurant,
            name=name
        ).exists():

            itemList = restaurant.items.all()

            return render(
                request,
                'delivery/update_menu.html',
                {
                    'restaurant': restaurant,
                    'itemList': itemList,
                    'error':
                    'This food item already exists in this restaurant.'
                }
            )

        # Create food item
        Item.objects.create(
            restaurant=restaurant,
            name=name,
            description=description,
            price=price,
            vegeterian=vegeterian,
            picture=picture
        )

        return redirect(
            'open_update_menu',
            restaurant_id=restaurant_id
        )

    return redirect(
        'open_update_menu',
        restaurant_id=restaurant_id
    )


# =========================================================
# CUSTOMER MENU
# =========================================================

def view_menu(
    request,
    restaurant_id,
    username
):

    restaurant = get_object_or_404(
        Restaurant,
        id=restaurant_id
    )

    itemList = restaurant.items.all()

    return render(
        request,
        'delivery/customer_menu.html',
        {
            'itemList': itemList,
            'restaurant': restaurant,
            'username': username
        }
    )


# =========================================================
# ADD TO CART
# =========================================================

def add_to_cart(
    request,
    item_id,
    username
):

    item = get_object_or_404(
        Item,
        id=item_id
    )

    customer = get_object_or_404(
        Customer,
        username=username
    )

    # Get existing cart or create new cart
    cart, _created = Cart.objects.get_or_create(
        customer=customer
    )

    # Add item
    cart.items.add(item)

    # Go to cart
    return redirect(
        'show_cart',
        username=username
    )


# =========================================================
# SHOW CART
# =========================================================

def show_cart(
    request,
    username
):

    customer = get_object_or_404(
        Customer,
        username=username
    )

    cart = Cart.objects.filter(
        customer=customer
    ).first()

    if cart:

        cart_items = cart.items.all()

        total_price = cart.total_price()

    else:

        cart_items = []

        total_price = 0

    return render(
        request,
        'delivery/cart.html',
        {
            'cart_items': cart_items,
            'total_price': total_price,
            'username': username
        }
    )


# =========================================================
# CHECKOUT
# =========================================================

def checkout(request, username):

    customer = get_object_or_404(
        Customer,
        username=username
    )

    cart = Cart.objects.filter(
        customer=customer
    ).first()

    if cart:
        cart_items = cart.items.all()
        total_price = cart.total_price()
    else:
        cart_items = []
        total_price = 0

    if total_price == 0:
        return render(
            request,
            'delivery/checkout.html',
            {
                'username': username,
                'cart_items': cart_items,
                'total_price': 0,
                'error': 'Your cart is empty!'
            }
        )

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    order_data = {
        'amount': int(total_price * 100),
        'currency': 'INR',
        'payment_capture': '1'
    }

    order = client.order.create(
        data=order_data
    )
    print("RAZORPAY KEY BEING SENT:", settings.RAZORPAY_KEY_ID)

    return render(
        request,
        'delivery/checkout.html',
        {
            'username': username,
            'cart_items': cart_items,
            'total_price': total_price,

            'razorpay_key_id':
                settings.RAZORPAY_KEY_ID,

            'order_id':
                order['id'],

            'amount':
                int(total_price * 100)
        }
    )

# =========================================================
# ORDERS / ORDER SUCCESS
# =========================================================

def orders(
    request,
    username
):

    customer = get_object_or_404(
        Customer,
        username=username
    )

    cart = Cart.objects.filter(
        customer=customer
    ).first()

    if cart:

        # Convert QuerySet to list
        # before clearing the cart
        cart_items = list(
            cart.items.all()
        )

        total_price = cart.total_price()

        # Clear cart
        cart.items.clear()

    else:

        cart_items = []

        total_price = 0

    return render(
        request,
        'delivery/orders.html',
        {
            'username': username,
            'customer': customer,
            'cart_items': cart_items,
            'total_price': total_price
        }
    )
