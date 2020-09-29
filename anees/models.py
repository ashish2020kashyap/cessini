from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    
 
    email = models.EmailField(blank=True)
    
 
    def __str__(self):
        return self.email



class Invalidmail(models.Model):

    email = models.EmailField(blank=True)
 
    def __str__(self):
        return self.email        


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True,blank=True)
    objects = models.Manager


    def __str__(self):
        return self.name



class Email(models.Model):
    my_customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, related_name='mycust')
    name = models.CharField(max_length=200, null=True)
    upload_file = models.FileField(upload_to='CSV', null=True, blank=True)



    def __str__(self):
        return self.name


class Campaign(models.Model):
    name = models.CharField(max_length=200, null=True)
    sender_name = models.CharField(max_length=200, null=True)
    sender_email = models.CharField(max_length=200, null=True)
    email_subject = models.CharField(max_length=200, null=True)
    my_customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, related_name='mycustomer')
    camp_emails = models.ForeignKey(Email, null=True, on_delete=models.SET_NULL, related_name='camp_email')




    def __str__(self):
        return self.name










class CampMail(models.Model):
    campaignings = models.OneToOneField(Campaign, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    camp = models.ManyToManyField(Email, related_name='emailings', null=True,blank=True)


    def __str__(self):
        return self.name



