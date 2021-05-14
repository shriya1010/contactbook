from django.db import models

class Contact_Book(models.Model):
    name=models.CharField(max_length=100,blank=False)
    email=models.EmailField()
    contact_number=models.BigIntegerField()
