from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class Item(models.Model):
    name=models.CharField(max_length=100,default='Juice')
    brandname=models.CharField(max_length=30,default='Pran')
    price=models.CharField(max_length=20,default='50')
    describe=models.CharField(max_length=100,default='String')

class Sell(models.Model):
    pname=models.CharField(max_length=30,default='Juice')
    pprice=models.DecimalField(max_digits=8,decimal_places=2)
    date=models.CharField(max_length=30,default='1/2/3')

