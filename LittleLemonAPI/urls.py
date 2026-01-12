from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('category',views.CategoriesView.as_view()),
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('cart/menu-items', views.CartView.as_view(), name='cart'),
    path('orders', views.OrderView.as_view(), name='orders'),
    path('orders/<int:pk>', views.SingleOrderView.as_view(), name='single-order'),
   
   
    path('groups/manager/users', views.ManagerUsersView.as_view(), name='manager-users'),
    path('groups/manager/users/<int:pk>', views.ManagerSingleUserView.as_view(), name='manager-single-user'),
    path('groups/delivery-crew/users', views.DeliveryCrewUsersView.as_view(), name='delivery-crew-users'),
    path('groups/delivery-crew/users/<int:pk>', views.DeliveryCrewSingleUserView.as_view(), name='delivery-crew-single-user'),
    # path("secret/", views.SecretView),
    # path('api-token-auth/', obtain_auth_token),
    # path('manager-view/', views.manager_view),
]
