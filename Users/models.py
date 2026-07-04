from django.db import models

class Customer(models.Model):
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    national_id = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    kyc_status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Verified', 'Verified')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    blockchain_tx = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} ({self.national_id})"