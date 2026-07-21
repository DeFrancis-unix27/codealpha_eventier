from django.db import models
import bcrypt
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.

class Custom_User(models.Model):
    firstname = models.CharField(max_length=20, blank=False, null=False)
    lastname = models.CharField(max_length=20, blank=False, null=False)
    user_email = models.EmailField(unique=True, blank=False, null=False)
    username = models.CharField(unique=True,max_length=25)
    password = models.CharField(max_length=30)

    def check_pass(self, hashed_pass):
        return check_password( hashed_pass, self.password )
    
    def save(self, *args, **kwags):
        if not self.password.startwith("bcrypt_sha256$") or self.password.startwith('pbkdf2_sha256$'):
           self.password = make_password(self.password)

        super.save(*args,*kwargs)

class Event(models.Model):
    event_orgs = models.ForeignKey(Custom_User,on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    banner = models.FileField(upload_to="event_banners/")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

class Custom_Field(models.Model):
    QUEST_TYPE=[
        ("FEEDBACK","Feedback"),
        ("REVIEW","Review"),
        ("REGULER","Reguler"),
        ("OTHER","Other")
    ]
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name='custom_field')
    cartegory = models.CharField(choices=QUEST_TYPE,max_length=20,default="REGULER")
    question = models.CharField(max_length=200)
    field_type = models.CharField(max_length=30,default="text") # can contain other options like date,chioce,number and others
    choice = models.TextField(blank=True,null=True) # if blank they use text but else use comma to differentiate chioces or number
    required = models.BooleanField(default=False) 
    order = models.IntegerField(default=0)    

class Attendee(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    user = models.ForeignKey(Custom_User,on_delete=models.CASCADE)
    reg_date = models.DateTimeField(auto_now_add=True)

class Custom_Answer(models.Model):
    attendee = models.ForeignKey(Attendee,on_delete=models.CASCADE)
    question = models.ForeignKey(Custom_Field,on_delete=models.CASCADE)
    answer = models.TextField()
    
