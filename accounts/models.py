from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission
import uuid
from django.utils import timezone

class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)
        username = email.split('@')[0]  # Generate username from email prefix
        
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.withdraw_password = self.make_random_password()
        user.save(using=self._db)
        
        
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **extra_fields)

class Account(AbstractBaseUser , PermissionsMixin):  # Inherit from PermissionsMixin
    email = models.EmailField(verbose_name="email", max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True, editable=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    fullname = models.CharField(max_length=200)
    phone = models.CharField(max_length=15,)
    country = models.CharField(max_length=50,)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        blank=True, 
        null=True, 
        default='profile_pics/profile_pic.webp'  # Set default image path
    )
    # Add groups and user_permissions fields
    groups = models.ManyToManyField(Group, related_name="accounts", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="accounts", blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Remove username from required fields
    
    objects = MyAccountManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def update_password(self, new_password):
        self.set_password(new_password)
        self.save()

    def get_profile_picture_url(self):
        """Returns the profile picture URL or default image URL if not uploaded"""
        if self.profile_picture:
            return self.profile_picture.url
        return '/media/profile_pics/profile_pic.webp'    
    
    

class Balance(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    usdt_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_profits = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # New field

    def __str__(self):
        return f"{self.user.username}'s USDT Balance"




class ForexPlan(models.Model):
    PERCENTAGE_CHOICES = [
        (5, '5%'),
        (69, '69%'),
        (120, '120%'),
        (200, '200%'),
    ]
    DURATION_CHOICES = [
        ('After 6 Hours', 'After 6 Hours'),
        ('Hourly', 'Hourly'),
        ('Daily', 'Daily'),
        ('For 8 Hours', 'For 8 Hours'),
        ('Weekly', 'Weekly'),
        ('After 3 Months', 'After 3 Months'),
        ('After 6 Months', 'After 6 Months'),
        ('Forever', 'Forever'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    percentage = models.IntegerField(choices=PERCENTAGE_CHOICES)
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES)
    min_amount = models.DecimalField(max_digits=10, decimal_places=2)
    max_amount = models.DecimalField(max_digits=10, decimal_places=2)
   
    def __str__(self):
        return f"{self.name} - {self.percentage}% - {self.duration}"







# Get the custom user model
User = settings.AUTH_USER_MODEL
class WalletAddress(models.Model):
    """User Wallet Address Model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallet_addresses")
    address = models.CharField(max_length=255, unique=True)
    currency = models.CharField(max_length=10, choices=[("BTC", "Bitcoin"), ("ETH", "Ethereum"),
                                                       ("USDT(TRC)", "USDT(TRC)"),("USDT(ETH)", "USDT(ETH)"), ("LTC", "Litecoin"),
                                                        ("TRX", "Tron"), ("BCH", "Bitcoin Cash")])

    def __str__(self):
        return f"{self.user.email} - {self.currency} Wallet"


class Referral(models.Model):
    """User Referral Model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="referral")
    email = models.EmailField(unique=True)
    referral_code = models.CharField(max_length=10, unique=True)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = uuid.uuid4().hex[:10].upper()  # Generate unique referral code
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Referral: {self.email} - {self.referral_code}"


class PaymentGateway(models.Model):
    """Payment Gateway Model"""
    wallet_address = models.CharField(max_length=255, unique=True)
    currency = models.CharField(max_length=10, choices=[("BTC", "Bitcoin"),("USDT(TRC)", "USDT(TRC)"),("USDT(ETH)", "USDT(ETH)")])
    def __str__(self):
        return f"Gateway - {self.currency}"


class DepositTransaction(models.Model):
    """User Deposit Transaction Model"""
    STATUS_CHOICES = [("pending", "Pending"), ("completed", "Completed"), ("failed", "Failed")]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="deposits")
    uniqid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    method = models.CharField(max_length=50)  # Payment method (e.g., Bank Transfer, PayPal, Crypto)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    tx_ref = models.CharField(max_length=100, unique=True)
    screenshot = models.ImageField(upload_to="deposit_screenshots/", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.user.email} - {self.amount} - {self.status}"


class WithdrawTransaction(models.Model):
    """User Withdrawal Transaction Model"""
    STATUS_CHOICES = [("pending", "Pending"), ("completed", "Completed"), ("failed", "Failed")]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="withdrawals")
    uniqid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    currency = models.CharField(max_length=10, choices=[("BTC", "Bitcoin"), ("ETH", "Ethereum"),
                                                        ("USDT(TRC)", "USDT(TRC)"),("USDT(ETH)", "USDT(ETH)"), ("LTC", "Litecoin"),
                                                        ("TRX", "Tron"), ("BCH", "Bitcoin Cash")])
    amount = models.DecimalField(max_digits=15, decimal_places=7)
    withdraw_address = models.CharField(max_length=255,null=True)
    tx_ref = models.CharField(max_length=100, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.user.email} - {self.currency} - {self.amount}"
        





class Users_Investment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uniq_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    profit = models.DecimalField(max_digits=15, decimal_places=2)
    daily_income = models.DecimalField(max_digits=15, decimal_places=2)
    total = models.DecimalField(max_digits=15, decimal_places=2)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    last_updated = models.DateTimeField(default=timezone.now)
     
    def ends_in(self):
        return (self.end_date - timezone.now()).days if self.end_date > timezone.now() else 0
    
    def elapsed(self):
        return (timezone.now() - self.start_date).days if self.start_date < timezone.now() else 0
    
    def __str__(self):
        return f"{self.title} - {self.user.email}"




class TransactionCodes(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("used", "Used"),
        ("expired", "Expired"),
        ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
        
    withdraw_code = models.CharField(max_length=6, blank=True, null=True)  # 6-digit withdrawal code
    withdraw_code_created_at = models.DateTimeField(auto_now=True)
    withdraw_code_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    
    reset_code = models.CharField(max_length=6, blank=True, null=True)  # 6-digit password reset code
    reset_code_created_at = models.DateTimeField(auto_now=True)
    reset_code_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    
    def __str__(self):
        return f"{self.user.username}'s Transaction Codes"
                


class TingaTingaPlan(models.Model):
    """Investment Plans for Tinga Tinga AI Trading Bot"""
        
    PERCENTAGE_CHOICES = [
        (5, '5% Daily'),
        (10, '10% Daily'),
        (15, '15% Daily'),  # Fixed the incorrect backtick
        (20, '20% Daily'),
    ]
        
    name = models.CharField(max_length=100, unique=True)
    percentage = models.IntegerField(choices=PERCENTAGE_CHOICES, help_text="Daily profit percentage")
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Minimum investment amount")
    max_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Maximum investment amount")
    duration_days = models.IntegerField(help_text="Duration of the plan in days")  
  
    def __str__(self):
        return f"{self.name} - {self.percentage}% Daily - {self.duration_days} Days"
    

        