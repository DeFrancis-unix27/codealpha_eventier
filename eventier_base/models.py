from django.db import models
import uuid
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, username, user_email, firstname, lastname, password=None):
        if not username:
            raise ValueError("Users must have a username")
        if not user_email:
            raise ValueError("Users must have an email address")
        if not firstname:
            raise ValueError("Users must have a first name")
        if not lastname:
            raise ValueError("Users must have a last name")

        user = self.model(
            username=username,
            user_email=self.normalize_email(user_email),
            firstname=firstname,
            lastname=lastname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, user_email, firstname, lastname, password):
        user = self.create_user(
            username=username,
            user_email=user_email,
            firstname=firstname,
            lastname=lastname,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    firstname = models.CharField(max_length=20, blank=False, null=False)
    lastname = models.CharField(max_length=20, blank=False, null=False)
    user_email = models.EmailField(unique=True, blank=False, null=False)
    slug = models.SlugField(max_length=300, blank=True, unique=True)
    username = models.CharField(unique=True, max_length=25)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["user_email", "firstname", "lastname", "password"]

    objects = CustomUserManager()

    def check_pass(self, hashed_pass):
        return check_password(hashed_pass, self.password)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def save(self, *args, **kwargs):
        if self.password == None:
            raise ValueError("Password cannot be None")
        if self.password != None:
            if self.password and not (
                str(self.password).startswith("bcrypt_sha256$")
                or str(self.password).startswith("pbkdf2_sha256$")
            ):
                self.password = make_password(self.password)

        if not self.slug:
            if self.username == None:
                fullname = f"{self.firstname} {self.lastname}"
                self.slug = slugify(fullname)
            else:
                self.slug = slugify(self.username)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Event(models.Model):
    STATUS = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("postponed", "Postponed"),
    ]
    event_orgs = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    slug = models.SlugField(max_length=300, blank=True, unique=True, null=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    banner = models.FileField(upload_to="event_banners/", blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    state = models.CharField(max_length=30, choices=STATUS, default="draft")
    postponed_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.postponed_date:
            self.state = "postponed"
        super().save(*args, **kwargs)


class Chioce(models.Model):
    title = models.CharField(max_length=20, unique=True)
    desc = models.TextField(max_length=400)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class CustomField(models.Model):
    QUEST_TYPE = [
        ("FEEDBACK", "Feedback"),
        ("REVIEW", "Review"),
        ("REGULER", "Reguler"),
        ("OTHER", "Other"),
    ]
    FIELD_TYPE = [
        ("NUMBER", "Number"),
        ("CHIOCE", "Chioce"),
        ("DATE", "Date"),
        ("TEXT", "Text"),
    ]
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="custom_field"
    )
    cartegory = models.CharField(choices=QUEST_TYPE, max_length=20, default="REGULER")
    question = models.CharField(max_length=200)
    field_type = models.CharField(
        choices=FIELD_TYPE, max_length=20, default="TEXT"
    )  # can contain other options like date,chioce,number and others
    choice = models.ForeignKey(
        Chioce, on_delete=models.CASCADE, related_name="chioce", blank=True, null=True
    )  # if blank they use text but else use comma to differentiate chioces or number
    required = models.BooleanField(default=False)
    order = models.IntegerField(default=0)


class Attendee(models.Model):
    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    firstname = models.CharField(max_length=255, null=True, blank=True)
    lastname = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True,null=True)
    is_guest = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwags):
        if not self.user:
            self.is_guest = True
        else:
            self.firstname = self.user.firstname
            self.lastname = self.user.lastname
            self.email = self.user.user_email
            self.is_guest = False
        return super().save(*args, **kwags)


class CustomAnswer(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    question = models.ForeignKey(CustomField, on_delete=models.CASCADE)
    answer = models.TextField()
