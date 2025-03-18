from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils.html import strip_tags
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_protect
import json
from django.contrib.auth.hashers import make_password,check_password
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
import os
from django.conf import settings
import shutil
from requests.exceptions import ConnectionError
import requests 
from django.contrib.auth.decorators import login_required
# from accounts.models import Transaction,Card
from django.db.models import Sum
from accounts.models import ForexPlan,PaymentGateway,DepositTransaction,WalletAddress,Users_Investment,WithdrawTransaction,TingaTingaPlan
from django.db.models import Sum


def home(request):    
    return render(request,'home/index.html')


def about(request):
    return render(request,'home/about.html')  


def plan(request):
    return render(request,'home/plan.html')      

def faq(request):
    return render(request,'home/faq.html')



def contact(request):
    return render(request,'home/contact_us.html')

def signup_view(request):
    return render(request,'forms/signup.html') 


def login_view(request):
    return render(request,'forms/login.html') 

def dash(request):
    if request.user.is_authenticated:
        investments_exist = Users_Investment.objects.filter(user=request.user).exists()
        if investments_exist:
            total_investment = Users_Investment.objects.filter(user=request.user).aggregate(total=Sum('total'))['total'] or 0.00
        else:
            total_investment = 0.00
        print(f"Total Investment for {request.user}: {total_investment}")  # Debugging
    else:
        total_investment = 0.00
    return render(request,'Dashboard/pages/index.html',{'total_investment': total_investment})             

def profile_view(request):
    return render(request,"Dashboard/pages/profile.html")    

def referals(request):
    return render(request,'Dashboard/pages/referrals.html')   

def Deposit_view(request):
    payment_gateways = PaymentGateway.objects.all()
    return render(request,'Dashboard/pages/Deposit.html',{"payment_gateways": payment_gateways})  

def Deposit_his_view(request):
    deposits = DepositTransaction.objects.filter(user=request.user).order_by("-date") 
    context = {
        'deposits': deposits
    }
    return render(request,'Dashboard/pages/Deposit_history.html',context)            

def purchase_plan(request):
    forex_plans = ForexPlan.objects.all()  
    tinga_tinga_plans = TingaTingaPlan.objects.all()  # Fetch Tinga Tinga plans
    
    return render(request, 'Dashboard/pages/purchase_plan.html', {
        'plans': forex_plans,
        'tinga_tinga_plans': tinga_tinga_plans  
    })

def view_plans(request):
    purchased_plans = Users_Investment.objects.filter(user=request.user).order_by('-start_date')
    return render(request,'Dashboard/pages/view_plan.html',{'purchased_plans': purchased_plans})            

def withdraw_view(request):
    wallet_addresses = WalletAddress.objects.filter(user=request.user)
    return render(request,'Dashboard/pages/withdraw.html',{'wallet_addresses': wallet_addresses})

def withdraw_history_view(request):
    withdrawals = WithdrawTransaction.objects.filter(user=request.user)
    return render(request,'Dashboard/pages/withdraw_history.html',{'withdrawals': withdrawals})
