from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Account(models.Model):
    
    ACCOUNT_CHOICE = (
        ('RRSP', 'Registered Retirement Savings Plan'),
        ('TFSA', 'Tax-Free Saving Account'),
        ('RESP', 'Registered Education Savings Plan'),
        ('MARGIN', 'Non-Registered Margin Account'),
    )

    BROKERAGE_CHOICE = (
        ('QTRADE', 'Qtrade Investor'),
        ('QUESTRADE', 'Questrade'),
        ('TD', 'TD Direct Investing'),
        ('NATIONAL BANK', 'National Bank Direct Brokerage'),
        ('SCOTIABANK', 'Scotia iTrade'),
        ('CIBC', 'CIBC Investor\'s Edge'),
        ('INTERACTIVE', 'Interactive Brokers'),
        ('WEALTHSIMPLE', 'WealthSimple'),
    )

    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=100, choices=ACCOUNT_CHOICE)
    brokerage = models.CharField(max_length=100, choices=BROKERAGE_CHOICE)
    cash_balance = models.FloatField(default=0.0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('account_detail', kwargs={'pk': self.pk})

class Security(models.Model):

    SECURITY_CHOICE = (
        ('CASH', 'Cash'),
        ('STOCK', 'Stock'),
        ('BOND', 'Bond'),
        ('OPTION', 'Option'),
        ('MUTUAL FUND', 'Mutual Fund'),
    )
    
    name = models.CharField(max_length = 100)
    ticker_symbol = models.CharField (max_length = 15)
    num_shares = models.FloatField(default = 1.0)
    security_type =  models.CharField(max_length=100, choices=SECURITY_CHOICE)
    date_of_purchase =  models.DateField()
    purchase_price = models.FloatField(default = 0.0)
    account = models.ForeignKey("Account", on_delete=models.CASCADE)

    def __str__(self):
        return self.ticker_symbol

    def get_absolute_url(self):
        return reverse('security_detail', kwargs={'pk': self.pk}) 