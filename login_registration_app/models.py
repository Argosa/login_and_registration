from __future__ import unicode_literals
import re # the regex module
from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        # add keys and values in to errors dictionary
        if len(postData['reg_first_name']) < 2:
            errors["reg_first_name"] = "Your name must be 2 characters or more "
        if len(postData['reg_last_name']) < 2:
            errors["reg_last_name"] = "Your last name must be at lease 2 characters"
        if not EMAIL_REGEX.match(postData['reg_email']):
            errors['reg_email'] = "Invalid email address!"
        if len(postData['reg_password']) < 8:
            errors["reg_password"] = "Your password must be 8 characters or more"
        if postData['reg_password'] != postData['reg_confirm']:
            errors["reg_confirm"] = "Your passwords must match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=90)
    last_name = models.CharField(max_length=90)
    user_email = models.CharField(max_length=255)
    password = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() # adds user manager to class

    def __repr__(self):   
        return f"first_name: {self.first_name} last_name: {self.last_name} email: {self.user_email} password: {self.password} created_at {self.created_at} updated_at {self.updated_at}"
