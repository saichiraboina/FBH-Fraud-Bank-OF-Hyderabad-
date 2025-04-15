from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name = 'index'),
    path('1',views.create,name = 'create'),
    path('2',views.pin_gen,name = 'pin'),
    path('otp',views.valid_otp ,name = 'OTP'),
    path('3',views.wallet,name = 'wallet'),
    path('4',views.deposite,name = 'deposite'),
    path('5',views.transaction,name = 'transaction'),
    path('6',views.withdraw,name = 'withdraw')
]