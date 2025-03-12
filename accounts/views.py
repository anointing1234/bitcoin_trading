from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
from django.contrib.auth import login,authenticate,get_user_model 
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import logout as auth_logout,login as auth_login,authenticate
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_protect
import json
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password,check_password
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
import os
from email.mime.image import MIMEImage
from django.conf import settings
import shutil
from django.utils.timezone import now
from requests.exceptions import ConnectionError
import requests 
import uuid
# from accounts.form  
# from .models import 
import random
from django.utils.crypto import get_random_string
from django.utils.timezone import now, timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from .models import Account 
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from .models import  WalletAddress,PaymentGateway,DepositTransaction,WithdrawTransaction,Balance,TransactionCodes,Users_Investment,ForexPlan

User = get_user_model()


def register(request):
    if request.method == "POST":
        try:
            # Parse JSON data (if sent as JSON)
            if request.content_type == "application/json":
                data = json.loads(request.body)
                email = data.get("email")
                password = data.get("password")
                confirm_password = data.get("confirmPassword")
            else:  # If form data (multipart/form-data)
                email = request.POST.get("user[email]")
                password = request.POST.get("user[password]")
                confirm_password = request.POST.get("user[confirmPassword]")

            if not email or not password or not confirm_password:
                return JsonResponse({'success': False, 'error': 'All fields are required!'})

            if password != confirm_password:
                return JsonResponse({'success': False, 'error': 'Passwords do not match!'})

            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'error': 'Email is already in use!'})

         
            # Create and save user
            user = User.objects.create_user(email=email,password=password)
            user.save()

            # Log in the user
            login(request, user)

            return JsonResponse({'success': True, 'message': 'Registration successful!'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Error: {str(e)}'})

    return render(request, 'forms/signup.html')




def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"success": True, "message": "Login successful!"})
        else:
            return JsonResponse({"success": False, "message": "Invalid email or password. Please try again."})

    return render(request, "forms/login.html")




def update_profile_picture(request):
    if request.method == "POST" and request.FILES.get("profile_picture"):
        user = request.user
        user.profile_picture = request.FILES["profile_picture"]
        user.save()
        messages.success(request, "Profile picture updated successfully!")
    else:
        messages.error(request, "No file selected. Please choose a valid image.")
    return render(request, "Dashboard/pages/profile.html")





def update_profile(request):
    if request.method == "POST":
        user = request.user
        email = request.POST.get("email", "").strip()
        fullname = request.POST.get("fullname", "").strip()
        country = request.POST.get("country", "").strip()
        phone = request.POST.get("phone", "").strip()

        # Update user profile fields
        user.email = email
        user.fullname = fullname
        user.country = country
        user.phone = phone
        user.save()

        messages.success(request, "Profile updated successfully!")
        return render(request, "Dashboard/pages/profile.html") # Change to your profile URL name

    return render(request, "Dashboard/pages/profile.html")


def update_password(request):
    if request.method == "POST":
        user = request.user
        current_password = request.POST.get("current_password", "").strip()
        new_password = request.POST.get("new_password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()
        # Check if current password is correct
        if not check_password(current_password, user.password):
            messages.error(request, "Current password is incorrect!")
            return render(request, "Dashboard/pages/profile.html")

        # Check if new password matches confirmation
        if new_password != confirm_password:
            messages.error(request, "New password and confirmation do not match!")
            return render(request, "Dashboard/pages/profile.html")

        # Update password
        user.set_password(new_password)
        user.save()

        # Keep user logged in after password change
        update_session_auth_hash(request, user)

        messages.success(request, "Password updated successfully!")
        return render(request, "Dashboard/pages/profile.html")
    return render(request, "Dashboard/pages/profile.html")





def update_withdrawal_account(request):
    if request.method == "POST":
        user = request.user
        wallet_address = request.POST.get("wallet_address", "").strip()
        currency = request.POST.get("currency", "").strip()

        # Ensure required fields are filled
        if not wallet_address or not currency:
            messages.error(request, "Wallet address and currency are required.")
            return render(request, "Dashboard/pages/profile.html")  # Redirect instead of render

        # Ensure valid currency selection
        valid_currencies = ["BTC", "ETH", "USDT_TRX", "USDT_ETH", "LTC", "TRX", "BCH"]
        if currency not in valid_currencies:
            messages.error(request, "Invalid currency selected.")
            return render(request, "Dashboard/pages/profile.html")

        # Update or create wallet address
        wallet, created = WalletAddress.objects.update_or_create(
            user=user, currency=currency,
            defaults={"address": wallet_address}
        )

        if created:
            messages.success(request, "Withdrawal account added successfully!")
        else:
            messages.success(request, "Withdrawal account updated successfully!")

        return redirect("profile")  # Redirect after updating

    return render(request, "Dashboard/pages/profile.html")


@csrf_exempt
def logout_view(request):
    """Logs out the user and redirects to the login page."""
    if request.method == "POST":
        auth_logout(request)
        request.session.flush()
        return redirect("home") 
    return redirect("home") 


def deposit_funds(request):
    payment_gateways = PaymentGateway.objects.all()  # Fetch once to avoid repeated queries

    if request.method == "POST":
        user = request.user
        payment_method = request.POST.get("payment_method", "").strip()
        deposit_amount = request.POST.get("deposit_amount", "").strip()
        payment_screenshot = request.FILES.get("payment_screenshot")

        # Validate input fields
        if not payment_method or not deposit_amount or not payment_screenshot:
            messages.error(request, "All fields are required.")
            return render(request, "Dashboard/pages/Deposit.html", {"payment_gateways": payment_gateways})

        # Validate deposit amount
        try:
            deposit_amount = float(deposit_amount)
            if deposit_amount <= 0:
                messages.error(request, "Deposit amount must be greater than zero.")
                return render(request, "Dashboard/pages/Deposit.html", {"payment_gateways": payment_gateways})
        except ValueError:
            messages.error(request, "Invalid deposit amount format.")
            return render(request, "Dashboard/pages/Deposit.html", {"payment_gateways": payment_gateways})

        # Fetch wallet address from PaymentGateway
        gateway = PaymentGateway.objects.filter(currency=payment_method).first()
        if not gateway:
            messages.error(request, f"No payment gateway found for {payment_method}.")
            return render(request, "Dashboard/pages/Deposit.html", {"payment_gateways": payment_gateways})

        # Generate a unique transaction reference
        tx_ref = f"DEP-{uuid.uuid4().hex[:10].upper()}"

        # Save the deposit transaction
        DepositTransaction.objects.create(
            user=user,
            method=payment_method,
            amount=deposit_amount,
            tx_ref=tx_ref,
            screenshot=payment_screenshot,
            status="pending",
        )

        messages.success(request, "Deposit request submitted successfully!")

        # ✅ Use redirect to make messages persist
        return redirect("Deposit")  # Ensure 'deposit_page' is the correct URL name for the deposit page

    return render(request, "Dashboard/pages/Deposit.html", {"payment_gateways": payment_gateways})



def confirm_deposit_view(request, pk):
    deposit = get_object_or_404(DepositTransaction, pk=pk)
    
    # Fetch balance using the user from DepositTransaction
    balance = get_object_or_404(Balance, user=deposit.user)
    
    if deposit.status != "completed":
        deposit.status = "completed"
        deposit.save()
        
        # Update user balance
        balance.usdt_balance += deposit.amount 
        balance.save()

        messages.success(request, f"Deposit {deposit.tx_ref} has been confirmed successfully.")
        messages.success(request, f"Balance update for {deposit.user} has been credited successfully.")
    else:
        messages.warning(request, f"Deposit {deposit.tx_ref} is already confirmed.")

    return redirect("admin:accounts_deposittransaction_changelist")






def decline_deposit_view(request, pk):
    deposit = get_object_or_404(DepositTransaction, pk=pk)

    if deposit.status == "pending":
        deposit.status = "declined"
        deposit.save()
        messages.error(request, f"Deposit {deposit.tx_ref} has been declined.")
    else:
        messages.warning(request, f"Deposit {deposit.tx_ref} cannot be declined as it is already {deposit.status}.")

    return redirect("admin:app_deposittransaction_changelist")





def send_pass_views(request):
    return render(request,'forms/send_reset_pass.html')

def reset_pass(request):
    return render(request,'forms/reset_pass.html')



def send_reset_code(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = get_object_or_404(Account, email=email)  # Check if user exists
        
        # Generate a 6-digit reset code
        reset_code = str(random.randint(100000, 999999))

        # Fetch or create TransactionCodes for the user
        transaction_code, created = TransactionCodes.objects.get_or_create(user=user)

        # Update reset code details
        transaction_code.reset_code = reset_code
        transaction_code.reset_code_created_at = now()
        transaction_code.reset_code_status = "active"
        transaction_code.save()

        # Send reset code via email
        send_mail(
            "Password Reset Code",
            f"Your password reset code is: {reset_code}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return JsonResponse({"success": True, "message": "Reset code sent to your email."})
    
    return JsonResponse({"success": False, "message": "Invalid request."})






def verify_reset_code(request):
    if request.method == "POST":
        email = request.POST.get("email")
        reset_code = request.POST.get("reset_code")
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not all([email, reset_code, new_password, confirm_password]):
            messages.error(request, "All fields are required.")
            return render(request, "forms/reset_pass.html")  # No redirect!

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "forms/reset_pass.html")  # No redirect!

        try:
            user = User.objects.get(email=email)
            transaction_code = TransactionCodes.objects.get(user=user)
        except User.DoesNotExist:
            messages.error(request, "No user found with this email.")
            return render(request, "forms/reset_pass.html")
        except TransactionCodes.DoesNotExist:
            messages.error(request, "Invalid reset code.")
            return render(request, "forms/reset_pass.html")

        # Ensure reset code is valid
        if (
            str(transaction_code.reset_code) != reset_code
            or transaction_code.reset_code_status != "active"
            or now() - transaction_code.reset_code_created_at > timedelta(minutes=20)
        ):
            messages.error(request, "Invalid or expired reset code.")
            return render(request, "forms/reset_pass.html")

        # Reset the password
        user.password = make_password(new_password)
        user.save()

        # Mark reset code as used
        transaction_code.reset_code_status = "used"
        transaction_code.save()

        messages.success(request, "Password reset successful. Please login.")
        return render(request, "forms/reset_pass.html")  # Render with messages

    return render(request, "forms/reset_pass.html")



def purchase_plan_view(request):
    if request.method == "POST":
        plan_id = request.POST.get("plan_id")
        amount = request.POST.get("amount")

        if not plan_id or not amount:
            messages.error(request, "Invalid plan selection!")
            return redirect("purchase_plan")

        # Convert amount to Decimal
        amount = Decimal(amount)

        # Fetch the selected plan
        plan = get_object_or_404(ForexPlan, id=plan_id)

        # Validate investment amount
        if amount < plan.min_amount or amount > plan.max_amount:
            messages.error(request, f"Investment amount must be between ${plan.min_amount} and ${plan.max_amount}!")
            return redirect("purchase_plan")

        # Check if user has an active investment in this plan
        existing_plan = Users_Investment.objects.filter(user=request.user, title=plan.name, status="active").exists()
        if existing_plan:
            messages.error(request, f"You already have an active '{plan.name}' plan. Wait until it expires before purchasing again.")
            return redirect("purchase_plan")

        # Get user's balance
        balance = Balance.objects.get(user=request.user)

        # Check if user has enough balance
        if balance.usdt_balance < amount:
            messages.error(request, "Insufficient balance to purchase this plan!")
            return redirect("purchase_plan")

        # Deduct the amount from user's balance
        balance.usdt_balance -= amount
        balance.save()

        # Calculate total profit and daily income
        total_profit = amount * (Decimal(plan.percentage) / Decimal(100))
        daily_income = total_profit / Decimal(30)  # Assuming a 30-day cycle

        # Create investment entry
        Users_Investment.objects.create(
            user=request.user,
            uniq_id=str(uuid.uuid4()),  # Unique ID for investment tracking
            title=plan.name,
            profit=total_profit,
            daily_income=daily_income,
            total=amount + total_profit,
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=30),  # Assuming a 30-day duration
            status="active",
        )

        messages.success(request, f"Plan '{plan.name}' purchased successfully!")
      
    return redirect("purchase_plan")



def withdraw_funds(request):
    user = request.user
    balance = Balance.objects.get(user=user)  # Get user's balance

    if request.method == "POST":
        withdraw_currency = request.POST.get("withdraw_currency")
        withdraw_address = request.POST.get("withdraw_address")
        withdraw_amount = request.POST.get("withdraw_amount")

        try:
            withdraw_amount = Decimal(withdraw_amount)
        except Exception:
            return JsonResponse({"success": False, "message": "Invalid withdrawal amount."})

        # Check if currency is selected
        if not withdraw_currency or not withdraw_address:
            return JsonResponse({"success": False, "message": "Please select a currency and enter a valid address."})

        # Check for sufficient balance
        if withdraw_amount > balance.usdt_balance:
            return JsonResponse({"success": False, "message": "Insufficient balance."})

        # Deduct from user's balance
        balance.usdt_balance -= withdraw_amount
        balance.save()

        # Create withdrawal transaction
        WithdrawTransaction.objects.create(
            user=user,
            currency=withdraw_currency,
            withdraw_address=withdraw_address,
            amount=withdraw_amount,
            tx_ref=str(uuid.uuid4()),  # Unique transaction reference
            status="pending"
        )

        return JsonResponse({"success": True, "message": "Withdrawal request submitted successfully."})

    # For GET requests, render the page as before
    return render(request, "Dashboard/pages/withdraw.html", {"balance": balance})



def send_withdrawal_code(request):
    user = request.user
    withdrawal_code = str(random.randint(100000, 999999))

    transaction_code, created = TransactionCodes.objects.get_or_create(user=user)
    transaction_code.withdraw_code = withdrawal_code
    transaction_code.withdraw_code_status = "active"
    transaction_code.save()

    # Send code via email
    send_mail(
        "Your Withdrawal Verification Code",
        f"Dear {user.username},\n\nYour withdrawal verification code is: {withdrawal_code}\n\nEnter this code to complete your withdrawal.",
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

    return JsonResponse({"success": True, "message": "A verification code has been sent to your email."})



def verify_withdrawal_code(request):
    if request.method == "POST":
        data = json.loads(request.body)
        entered_code = data.get("code")
        user = request.user

        transaction_code = TransactionCodes.objects.filter(user=user, withdraw_code_status="active").first()

        if transaction_code and entered_code == transaction_code.withdraw_code:
            transaction_code.withdraw_code_status = "used"
            transaction_code.save()
            return JsonResponse({"success": True, "message": "Code verified. You can now proceed with withdrawal."})
        
        return JsonResponse({"success": False, "message": "Invalid code. Please try again."})

    return JsonResponse({"success": False, "message": "Invalid request."})





def confirm_withdraw(request, withdraw_id):
    """Confirm a pending withdrawal."""
    withdrawal = get_object_or_404(WithdrawTransaction, pk=withdraw_id)
    if withdrawal.status == "pending":
        withdrawal.status = "completed"
        withdrawal.save()
        messages.success(request, f"Withdrawal {withdrawal.tx_ref} confirmed successfully!")
    else:
        messages.warning(request, "This withdrawal is not pending.")
    # Change 'withdrawtransaction_list' to the URL name where you list withdrawals.
    return redirect("admin:accounts_withdrawtransaction_changelist")

def decline_withdraw(request, withdraw_id):
    """Decline a pending withdrawal and refund the user."""
    withdrawal = get_object_or_404(WithdrawTransaction, pk=withdraw_id)
    if withdrawal.status == "pending":
        withdrawal.status = "failed"
        # Refund the user
        balance = Balance.objects.get(user=withdrawal.user)
        balance.usdt_balance += withdrawal.amount
        balance.save()
        withdrawal.save()
        messages.error(request, f"Withdrawal {withdrawal.tx_ref} declined and refunded!")
    else:
        messages.warning(request, "This withdrawal is not pending.")
    # Change 'withdrawtransaction_list' to the URL name where you list withdrawals.
    return redirect("admin:accounts_withdrawtransaction_changelist")





def send_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            full_name = data.get('fullName')
            user_email = data.get('email')
            phone = data.get('phone')
            amount_lost = data.get('amountLost')
            asset_type = data.get('assetType')
            incident_description = data.get('incidentDescription')

            subject = "New Asset Recovery Application"
            message = (
                f"Full Name: {full_name}\n"
                f"Email: {user_email}\n"
                f"Phone: {phone}\n"
                f"Amount Lost: {amount_lost}\n"
                f"Asset Type: {asset_type}\n"
                f"Incident Description: {incident_description}"
            )
            
            # Set the sender email as the user's email from the form
            from_email = settings.DEFAULT_FROM_EMAIL  # e.g., noreply@yourdomain.com
            # Admin email (or recipient) should be in a list
            recipient_list = [settings.DEFAULT_FROM_EMAIL]

            send_mail(subject, message, from_email, recipient_list)
            return JsonResponse({"success": True})
        except Exception as e:
            print("Error:", e)
            return JsonResponse({"success": False})
    return JsonResponse({"success": False})




