from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view , renderer_classes, permission_classes
from .models import MenuItem, Category, Cart , Order, OrderItem
from .serializers import MenuItemSerializer, CategorySerializer, CartSerializer, OrderItemSerializer, OrderSerializer, UserSerializer
from .permissions import IsManager, IsDeliveryCrew, IsCustomer

from rest_framework.permissions import IsAuthenticated
from .throttles import TenCallsPerMinute, FiveCallsPerMinute, TwoCallsPerMinute
from datetime import date
from django.contrib.auth.models import User, Group


# Create your views here.
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    throttle_classes = [TenCallsPerMinute]

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    filterset_fields = ['price','inventory']
    search_fields = ['category','title']
    throttle_classes = [TenCallsPerMinute] 


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    throttle_classes = [TenCallsPerMinute]


class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [TenCallsPerMinute]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        try:
            menuitem_id = request.data.get('menuitem_id')
            quantity = int(request.data.get('quantity', 1))
            
            
            menuitem = MenuItem.objects.get(pk=menuitem_id)
            
            
            unit_price = menuitem.price
            price = unit_price * quantity
            
            
            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                menuitem=menuitem,
                defaults={
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'price': price
                }
            )
            
            
            if not created:
                cart_item.quantity += quantity
                cart_item.price = cart_item.unit_price * cart_item.quantity
                cart_item.save()
            
            serializer = self.get_serializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except MenuItem.DoesNotExist:
            return Response(
                {"error": "Menu item not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def delete(self, request, *args, **kwargs):
        Cart.objects.filter(user=request.user).delete()
        return Response(
            {"message": "All cart items deleted"},
            status=status.HTTP_204_NO_CONTENT
        )

class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [FiveCallsPerMinute]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif user.groups.filter(name='Delivery Crew').exists():
            return Order.objects.filter(delivery_crew=user)
        else:
            return Order.objects.filter(user=user)
    
    def create(self, request, *args, **kwargs):
        
        cart_items = Cart.objects.filter(user=request.user)
        
        if not cart_items.exists():
            return Response(
                {"message": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
      
        total = sum(item.price for item in cart_items)
        
        
        order = Order.objects.create(
            user=request.user,
            total=total,
            date=date.today(),
            status=False
        )
        
        
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                menuitem=cart_item.menuitem,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                price=cart_item.price
            )
        
     
        cart_items.delete()
        
       
        serializer = self.get_serializer(order)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [FiveCallsPerMinute]
    
    def get_queryset(self):
        user = self.request.user
        
       
        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        
        
        elif user.groups.filter(name='Delivery Crew').exists():
            return Order.objects.filter(delivery_crew=user)
        
       
        else:
            return Order.objects.filter(user=user)
    
    def update(self, request, *args, **kwargs):
        order = self.get_object()
        user = request.user
        
      
        if user.groups.filter(name='Manager').exists():
            return super().update(request, *args, **kwargs)
        
        
        elif user.groups.filter(name='Delivery Crew').exists():
            if 'status' in request.data:
                order.status = request.data['status']
                order.save()
                return Response(
                    {"message": "Order status updated"},
                    status=status.HTTP_200_OK
                )
            return Response(
                {"message": "You can only update status"},
                status=status.HTTP_403_FORBIDDEN
            )
        
       
        else:
            return Response(
                {"message": "You cannot update orders"},
                status=status.HTTP_403_FORBIDDEN
            )
    
    def delete(self, request, *args, **kwargs):
        
        if request.user.groups.filter(name='Manager').exists():
            return super().delete(request, *args, **kwargs)
        
        return Response(
            {"message": "Only managers can delete orders"},
            status=status.HTTP_403_FORBIDDEN
        )

class ManagerUsersView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManager]
    throttle_classes = [TwoCallsPerMinute]
    
    def perform_create(self, serializer):
        user = User.objects.get(username=self.request.data['username'])
        managers_group = Group.objects.get(name='Manager')
        managers_group.user_set.add(user)

class ManagerSingleUserView(generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManager]
    throttle_classes = [TwoCallsPerMinute]
    
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        managers_group = Group.objects.get(name='Manager')
        managers_group.user_set.remove(user)
        return Response(
            {"message": "User removed from Manager group"},
            status=status.HTTP_200_OK
        )

class DeliveryCrewUsersView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name='Delivery Crew')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManager]
    throttle_classes = [TwoCallsPerMinute]
    
    def perform_create(self, serializer):
        user = User.objects.get(username=self.request.data['username'])
        delivery_group = Group.objects.get(name='Delivery Crew')
        delivery_group.user_set.add(user)

class DeliveryCrewSingleUserView(generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name='Delivery Crew')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManager]
    throttle_classes = [TwoCallsPerMinute]
    
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        delivery_group = Group.objects.get(name='Delivery Crew')
        delivery_group.user_set.remove(user)
        return Response(
            {"message": "User removed from Delivery Crew group"},
            status=status.HTTP_200_OK
        )



# @api_view()
# @permission_classes([IsAuthenticated])
# def SecretView(request):
#     return Response({"message":"Some secret message"})


# @api_view()
# @permission_classes([IsAuthenticated])
# def manager_view(request):
#     if request.user.groups.filter(name='Manager').exists():
#         return Response({"message": "Only manager should see this"})
#     else:
#         return Response({"message": "You are not authorized"}, 403)