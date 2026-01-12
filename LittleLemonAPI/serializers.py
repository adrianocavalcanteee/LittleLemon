from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, OrderItem
from django.contrib.auth.models import User



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title']

class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only =True)
    category  = CategorySerializer(read_only = True)
   
    class Meta:
        model = MenuItem
        fields =['id', 'title', 'price', 'inventory', 'category', 'category_id']

        extra_kwargs = {
            'price': {
                'min_value': 2
            },
            'inventory':{
                'min_value':0
            }
        }

class CartSerializer(serializers.ModelSerializer):
    menuitem= MenuItemSerializer(read_only=True)
    menuitem_id=serializers.IntegerField(write_only = True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'menuitem_id', 'quantity', 'unit_price']
        read_only_fields = ['user']
        
class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'menuitem', 'quantity', 'unit_price', 'price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']