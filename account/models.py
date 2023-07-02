from django.db import models
import uuid


from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)










# custom user manager
class MyUserManager(BaseUserManager):
    def create_user(self, email,password):
        """
        Creates and saves a User with the given email, otp and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email = self.normalize_email(email),
            password = password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# custom user model
class vendorregistration(AbstractBaseUser):

    email = models.EmailField('email',max_length=255,unique=True)
    password = models.CharField(max_length=20, blank=False, null=False)
    otp = models.CharField(max_length=8, null=True, blank=True)
    uid = models.UUIDField(default=uuid.uuid4)
    Otpcreated_at = models.DateTimeField(null=True, blank=True)
    Is_Approved= models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


# Create your models here.

# class vendorregistration(models.Model):
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=20, blank=False, null=False)
#     otp = models.CharField(max_length=8, null=True, blank=True)
#     uid = models.UUIDField(default=uuid.uuid4)
#     Otpcreated_at = models.DateTimeField(null=True, blank=True)
#     Is_Approved= models.BooleanField(default=False)
#     is_verified =models.BooleanField(default=False)


class VendorProfile(models.Model):
    vendor = models.ForeignKey(vendorregistration, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='images/',null = True,blank =True)
    age = models.IntegerField()
    city = models.CharField(max_length=255)
    working_or_studying = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)


class VendorArtwork(models.Model):
    vendor = models.ForeignKey(vendorregistration, on_delete=models.CASCADE)
    Art_image = models.ImageField(upload_to='images/',null = True, blank =True)
    themes = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    medium = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)



class users(models.Model):
    panting = models.ForeignKey(VendorArtwork, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile_number = models.BigIntegerField()
    Address = models.CharField(max_length=500)

      



def __str__(self):
    return f"Artwork by {self.vendor.name}"



def __str__(self):
        return self.name



@property
def imageURL(self):
    try:
        url = self.profile_picture.url
    except:
        url = ''
    return url

