from django.db import models
from datetime import datetime
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'

        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'
        
        if len(postData['email']) == 0:
            errors['email'] = "Email is required"
        elif not EMAIL_REGEX.match(postData['email']):    #check format of email
            errors['email'] = 'Invalid Email Address'
        
        existing_user = User.objects.filter(email=postData['email'])
        if len(existing_user) !=0:
            errors['user'] = "Email already in use"
        
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'        
        elif postData['password'] != postData['confirm_pw']:
            errors['password'] = 'Password and Confirm Password must match'  #don't tell them which one is wrong!
        
        return errors
      
    def login_validator(self, postData):
        errors = {}
        if len(postData['email']) == 0:
            errors['email'] = 'Email is required'
        elif not EMAIL_REGEX.match(postData['email']):    #check format of email
            errors['email'] = 'Invalid Email Address'
    
        existing_user = User.objects.filter(email=postData['email'])
        if len(existing_user) !=1:      #now checking that at least one is found
            errors['email'] = "User not found"
        else:
            if len(postData['password']) < 8:
                errors['password'] = 'Password must be at least 8 characters' 
                
            else :    
                if bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:  #authenticate
                    errors['email'] = 'Email and Password do not match'  #don't tell them which one is wrong!
            
        return errors
    

class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    @ property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_date(self):
        return self.created_at.date()
    
#-------------------end of USER ---------------------------------------------------------

#----add your new models here----

class ChildManager(models.Manager):
    def child_validator(self, postData):

        errors = {}
        #print(postData)

        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'

        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'
        
        if len(postData['birth_date']) == 0:
            errors['birth_date'] = "Please fill out child's birth date"

        if "child_gender" not in postData or len(postData['child_gender']) ==0:
            errors['child_gender'] = 'Please fill out the gender of your child'

        if len(postData['child_grade']) == 0:
            errors['child_grade'] = 'Please fill out the grade of the child'
        
        return errors

class Child(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateTimeField()
    gender = models.CharField(max_length=10)
    grade = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_child = models.ForeignKey(User, related_name="enrolled_parent",on_delete=models.CASCADE)  #OneParentManyChildren and ManyChildren can belong to OneParent
    objects = ChildManager()
    def __str__(self):
        return self.first_name

  

class Event(models.Model):
    event_name = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    event_date= models.DateField ()
    event_time= models.TimeField()
    max_capacity= models.IntegerField()
    action_enrolled=models.BooleanField(default=False)
    action_class_full=models.BooleanField(default=False)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=2)
    zip_code= models.CharField(max_length=5)
    child_event= models.ManyToManyField(Child, related_name='enrolled_child')
    user_event=models.ManyToManyField(User, related_name='enrolled_user') 
    def __str__(self):
        return self.event_name

    
#---end of adding new models


class Message(models.Model):    
    msg_content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    msg_UsrJoin = models.ForeignKey(User, related_name="usermessages_join",on_delete=models.CASCADE)    #OneUserManyMessages
    user_likes = models.ManyToManyField(User, related_name='liked_posts')                      #ManyUsersLikeManyMessages and ManyMessagesAreLikedbyManyUsers


class Comment(models.Model):    
    com_content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    com_UserJoin = models.ForeignKey(User, related_name="usercomments_join",on_delete=models.CASCADE)   #OneUserManyComments
    msg_CommJoin = models.ForeignKey(Message, related_name="msgcomments_join",on_delete=models.CASCADE) #OneMsgManyComments

