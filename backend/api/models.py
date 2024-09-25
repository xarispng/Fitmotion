from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    #username: A unique identifier for the user. It's a required field, with a default max length of 150 characters.
    #password: A hashed representation of the user's password. Django handles the hashing process, ensuring that passwords are stored securely.
    #is_active: A boolean field that designates whether this user account should be considered active. Unchecking this will prevent the user from logging in.
    #is_superuser: A boolean field indicating whether the user has all permissions without explicitly assigning them. This is used for superuser accounts that have all possible privileges.
    
    SEX_CHOICES = [('MALE', 'Male'),('FEMALE', 'Female'),]
    PAY_PLAN_CHOICES = [('MONTHLY', 'Monthly'),('4WEEK', '4Week'),]

    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES)
    sessions_per_week = models.IntegerField(null=True, validators=[MinValueValidator(0), MaxValueValidator(20)])
    phone = models.CharField(null=True, max_length=10, validators=[RegexValidator(r'^\d{10}$')])
    pay_plan = models.CharField(null=True, default='MONTHLY', max_length=7, choices=PAY_PLAN_CHOICES)
    next_payment = models.DateField(null=True)
    temp_sessions = models.IntegerField(null=True, default=2, validators=[MinValueValidator(0), MaxValueValidator(2)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'surname'], name='unique_name_surname')
        ]

class Session(models.Model):
    SEX_CHOICES = [('MALE', 'Male'),('FEMALE', 'Female'),]

    session_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES)
    hour = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(23)])
    date = models.DateField()
    fixed = models.BooleanField(default=False) 

class FixedSession(models.Model):
    fixed_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hour = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(23)])
    day = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(6)])

class DisabledDate(models.Model):
    ddate_id = models.AutoField(primary_key=True)
    hour = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(23)])
    date = models.DateField()
    whole_day = models.BooleanField(default=False)

class Reschedules(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    reschedules = models.IntegerField(default=3)