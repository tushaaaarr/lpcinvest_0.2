from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
from datetime import datetime
# from django.contrib.auth import get_user_model
# User = get_user_model()
from django.db.models.signals import post_save
from django.dispatch import receiver
from geopy.geocoders import Nominatim

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)


PROP_TYPE_CHOICES =(
    ("1", "studio"),
    ("2", "apartment"),
    )

FURNITURE_TYPE_CHOICES =(
    ("1", "room"),
    ("2", "bathrooms"),
    ("3", "garage"),
    )

# CITIES_CHOICES = PropertyCities.objects.all().values_list('name', flat=True)
# CITIES_CHOICES = tuple(CITIES_CHOICES)

CITIES_CHOICES = (
    ("1", "birmingham"),
    ("2", "	bolton"),
    ("3", "leeds"),
    ("4", "manchester"),
    ("5", "liverpool"),
    ("6", "london"),
    ("7", "sheffield"),
    ("8","bradford"),
    ("9","preston"),
    ("10","nottingham")

    )


class PropertyCities(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name


class Properties(models.Model):
    is_underconstruction = models.BooleanField(default=False)
    is_exclusive = models.BooleanField(default=False)

    # Basic Information
    title = models.CharField(max_length=30)
    type = models.CharField(max_length=10,choices=PROP_TYPE_CHOICES)
    price = models.IntegerField(default=0)
    yields = models.CharField(blank=True,max_length=40)
    area = models.CharField(blank=True,max_length=40)
    deposited_price = models.IntegerField(blank=True,default=0)
    # Location
    adddress = models.CharField(max_length=50)
    city = models.CharField(max_length=20,choices = CITIES_CHOICES)

    postal_code = models.CharField(max_length=10)
    lat = models.FloatField(blank=True)
    lon = models.FloatField(blank=True)

    # Detailed Information
    content = HTMLField()

    # Media
    image = models.FileField(upload_to = 'media')
    year_built = models.CharField(max_length=10)
    embedded_link_youtube = models.CharField(max_length=100)
    pub_date = models.DateField(default=datetime.now())

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.capitalize()
        self.adddress = self.adddress.capitalize()
        self.city = self.city.lower()
        loc = self.adddress
        geolocator = Nominatim(user_agent="my_request")
        location = geolocator.geocode(loc)
        try:
            self.lat = location.latitude
            self.lon = location.longitude
        except:
            self.lat = self.lat
            self.lon = self.lon
        try:
            self.deposited_price = int(self.area) / 100 * self.price
        except:
            pass
        return super(Properties, self).save(*args, **kwargs)


class FeatureMaster(models.Model):
    feature = models.CharField(max_length=40)
    def __str__(self):
        return str(self.feature)
    def save(self, *args, **kwargs):
        self.feature = self.feature.capitalize()
        return super(FeatureMaster, self).save(*args, **kwargs)

class PropertyTypeMaster(models.Model):
    type = models.CharField(max_length=20)
    def __str__(self):
        return str(self.type)
    
class PropertyTypeMapper(models.Model):
    property = models.ForeignKey(Properties, default=None, on_delete=models.CASCADE)
    type = models.ForeignKey(PropertyTypeMaster, default=None, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.property.title)


class PropertyFeatureMapper(models.Model):
    property = models.ForeignKey(Properties, default=None, on_delete=models.CASCADE)
    feature = models.ForeignKey(FeatureMaster, default=None, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.property.title)


class FurnitureMaster(models.Model):
    furniture_counts = models.CharField(max_length=5)
    def __str__(self):
        return self.furniture_counts


class PropertyFurnitureMapper(models.Model):
    property = models.ForeignKey(Properties, default=None, on_delete=models.CASCADE)
    furniture_counts = models.ForeignKey(FurnitureMaster, default=None, on_delete=models.CASCADE)
    furniture_type = models.CharField(max_length=10,choices=FURNITURE_TYPE_CHOICES)
    def __str__(self):
        return str(self.property.title)


class StatusMaster(models.Model):
    status = models.CharField(max_length=20)
    def __str__(self):
        return self.status
    def save(self, *args, **kwargs):
        self.status = self.status.capitalize()
        return super(StatusMaster, self).save(*args, **kwargs)


class PropertyStatusMapper(models.Model):
    property = models.ForeignKey(Properties, default=None, on_delete=models.CASCADE)
    status = models.ForeignKey(StatusMaster, default=None, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.property.title)


class UserFavProperties(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    is_checked = models.BooleanField(default=False)
    property = models.ForeignKey(Properties, default=None, on_delete=models.CASCADE)
    def __str__(self):
        return f"{str(self.user)} + {self.property.title}"


class UserExclusiveProperties(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    property = models.ForeignKey(Properties, default=None, on_delete=models.CASCADE)
    def __str__(self):
        return f"{str(self.user)} + {self.property.title}"

    def save(self, *args, **kwargs):
        property = Properties.objects.get(id = self.property.id)
        property.is_underconstruction = True
        property.is_exclusive=True
        property.save()
        return super(UserExclusiveProperties, self).save(*args, **kwargs)


class Discount(models.Model):
    value = models.IntegerField(default=0, verbose_name="Value")
    is_percentage = models.BooleanField(default=False, verbose_name="Is percentage?")
    def __str__(self):
        if self.is_percentage:
            return "{0}% - Discount".format(self.value)
        return "${0} - Discount".format(self.value)

    class Meta:
        verbose_name = "Discount"
        verbose_name_plural = "Discounts"

class PropertyOffers(models.Model):
    title = models.CharField(max_length=100)
    property = models.ForeignKey(Properties, default=None, on_delete=models.CASCADE)
    # user = models.ForeignKey(Properties, default=None, on_delete=models.CASCADE)
    is_automaically = models.BooleanField(default=False)
    discount =  models.ForeignKey('Discount', on_delete=models.CASCADE)

    def __str__(self):
        return (str(self.title))

class PropertyImage(models.Model):
    property = models.ForeignKey(Properties, default=None, on_delete=models.CASCADE)
    images = models.FileField(upload_to = 'media')
    def __str__(self):
        return self.property.title

from django_resized import ResizedImageField

class DownloadableAssets(models.Model):
    title = models.CharField(max_length=30)
    image = ResizedImageField(size=[300, 180], upload_to = 'media/download_assets')
    desc = models.TextField(default = " ",blank=True)
    downloadable_url = models.URLField(max_length=200)

    def __str__(self):
        return self.title


class ConstructionUpdates(models.Model):
    property = models.ForeignKey(Properties, default=None, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    desc = models.TextField(default = " ",blank=True)
    pub_date = models.DateField(default=datetime.now())

    def __str__(self):
        return self.title


class ConstructionUpdatesImage(models.Model):
    property_update_id = models.ForeignKey(ConstructionUpdates, default=None, on_delete=models.CASCADE)
    images = models.FileField(upload_to = 'media/property_updates')
    def __str__(self):
        return self.property_update_id.title



class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    fname = models.CharField(max_length=20, blank=True)
    lname = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=20, blank=True)
    def __str__(self):
        return self.fname

# Signals used to create profile instance
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,
        fname=instance.first_name,lname=instance.last_name,email=instance.email)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except:
        pass


class TeamMembers(models.Model):
    image = models.FileField(upload_to = 'media/team')
    name = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=30, blank=True)
    desc = models.TextField(default="")
    mobile = models.CharField(max_length=15, blank=True)
    email = models.CharField(max_length=40, blank=True)
    address = models.CharField(max_length=50, blank=True)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        return super(TeamMembers, self).save(*args, **kwargs)
    
    

class Blogs(models.Model):
    title = HTMLField()
    # title_t = models.CharField(max_length=100,default=" ")
    content = HTMLField()
    desc = models.TextField(default="")
    city = models.CharField(max_length=20,choices = CITIES_CHOICES)
    image_1 = models.FileField(upload_to = 'media/blogs')
    image_2 = models.FileField(upload_to = 'media/blogs')
    pub_date = models.DateField(default=datetime.now())
    def __str__(self):
        return self.desc
    def save(self, *args, **kwargs):
        self.name = self.title.capitalize()
        return super(Blogs, self).save(*args, **kwargs)
    