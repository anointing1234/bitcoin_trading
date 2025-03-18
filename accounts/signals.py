from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account,Balance,DepositTransaction
from decimal import Decimal  # Import Decimal for handling currency values
import uuid 

@receiver(post_save, sender=Account)
def create_user_balance(sender, instance, created, **kwargs):
    if created:  # Runs only when a new user is created
        # Create a balance entry for the new user with a $30 USDT balance
        balance = Balance.objects.create(user=instance, usdt_balance=Decimal('30.00'))
        
        # Create an initial deposit transaction
        DepositTransaction.objects.create(
            user=instance,
            method="Bonus Credit",  # Define the method (since it's not a real deposit)
            amount=Decimal('30.00'),
            tx_ref=str(uuid.uuid4()),  # Generate a unique transaction reference
            status="completed",  # Mark the transaction as successful
        )
