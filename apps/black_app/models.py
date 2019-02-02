from django.db import models
import re

class Validuser(models.Manager):
   
    def registerValidator(self, postData):
        errors = []
        if len(postData['fname']) < 3:
            errors.append('First name should be at least 2 characters')
        if len(postData['lname']) < 3:
            errors.append('Last name  should be at least 2 characters')
        if not re.match(r"[^@]+@[^@]+\.[^@]+", postData['email']):
            errors.append('Email is invalid')
        else:
            checkexist = User.objects.filter(email=postData['email'])
            if len(checkexist) > 0:
                errors.append('Email already exists')
        if len(postData['password']) < 8:
            errors.append('Password should be at least 8 characters')
        if postData['password'] != postData['confirm_password']:
            errors.append('Pw and confirmation do not match')

        zebra = {
            'errors': errors,
            'valid': True,
            'user': None
        }

        if len(errors) > 0:
            zebra['valid'] = False
        else:
            user = User.objects.create(
                first_name = postData['fname'],
                last_name = postData['lname'],
                email= postData['email'],
                password= postData['password']
            )
            zebra['user'] = user

        return zebra

    def loginValidator(self, postData):
        errors = []
        response = {
            'errors': errors,
            'valid': True,
            'user': None
        }
        match_list = User.objects.filter(email=postData['email'])
        if len(match_list)>0:                                                                                                         
            banana = match_list[0]
            if banana.password == postData['password']:
                response['user'] = banana
            else:
                errors.append('Not the right password')
        else:
            errors.append('Not existing email')
            response['valid']=False

        if len(errors) > 0:
            response['errors'] = errors
            response['valid'] = False
        return response


class User(models.Model):
    # id is a variable that is created for us
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    objects = Validuser() 
    def __repr__(self):
        return f"{self.first_name} {self.last_name} {self.email} {self.password} {self.password}"

class Job(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, related_name="jobs_uploaded")
    added_by = models.ForeignKey(User, related_name="added_jobs", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)