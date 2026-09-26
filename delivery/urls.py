
from django.urls import path
from . import views


urlpatterns = [

    # =========================
    # HOME
    # =========================

    path(
        '',
        views.index,
        name='index'
    ),


    # =========================
    # AUTHENTICATION
    # =========================

    path(
        'signin/',
        views.open_signin,
        name='open_signin'
    ),

    path(
        'signin/user/',
        views.signin,
        name='signin'
    ),

    path(
        'signup/',
        views.open_signup,
        name='open_signup'
    ),

    path(
        'signup/user/',
        views.signup,
        name='signup'
    ),


    # =========================
    # CUSTOMER
    # =========================

    path(
        'customer/<str:username>/',
        views.customer_home,
        name='customer_home'
    ),


    # =========================
    # ADMIN
    # =========================

    path(
        'admin-home/',
        views.admin_home,
        name='admin_home'
    ),


    # =========================
    # RESTAURANT
    # =========================

    path(
        'restaurant/add/',
        views.open_add_restaurant,
        name='open_add_restaurant'
    ),

    path(
        'restaurant/add/save/',
        views.add_restaurant,
        name='add_restaurant'
    ),

    path(
        'restaurants/',
        views.open_show_restaurant,
        name='open_show_restaurant'
    ),

    path(
        'restaurant/update/<int:restaurant_id>/',
        views.open_update_restaurant,
        name='open_update_restaurant'
    ),

    path(
        'restaurant/update/<int:restaurant_id>/save/',
        views.update_restaurant,
        name='update_restaurant'
    ),

    path(
        'restaurant/delete/<int:restaurant_id>/',
        views.delete_restaurant,
        name='delete_restaurant'
    ),


    # =========================
    # MENU
    # =========================

    path(
        'restaurant/menu/manage/<int:restaurant_id>/',
        views.open_update_menu,
        name='open_update_menu'
    ),

    path(
        'restaurant/menu/update/<int:restaurant_id>/',
        views.update_menu,
        name='update_menu'
    ),

    path(
        'menu/<int:restaurant_id>/<str:username>/',
        views.view_menu,
        name='view_menu'
    ),


    # =========================
    # CART
    # =========================

    path(
        'cart/add/<int:item_id>/<str:username>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/<str:username>/',
        views.show_cart,
        name='show_cart'
    ),


    # =========================
    # CHECKOUT
    # =========================

    path(
        'checkout/<str:username>/',
        views.checkout,
        name='checkout'
    ),


    # =========================
    # ORDERS
    # =========================

    path(
        'orders/<str:username>/',
        views.orders,
        name='orders'
    ),
]