from django.db import models
from django.conf import settings

# Create your models here.


def blog_upload(instance, filename):
 file_path = 'Properte/{catagory}/{title}/-{filename}'.format(
     catagory=str(instance.catagory.name),title=str(instance.title),  filename=filename
 )
def uplaod_lucation(instance, filename):
 file_path = 'Properte/{proper}/-{filename}'.format(
     proper=str(instance.proper.title),  filename=filename
 )
 return file_path

def uplaod_lucationn(instance, filename):
 file_path = 'Properte/{proper}/-{filename}'.format(
     proper=str(instance.title),  filename=filename
 )
 return file_path



class City(models.Model):
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name

class aria(models.Model):
  name = models.CharField(max_length=100) 
  city =models.ForeignKey(City ,on_delete=models.CASCADE)

  def __str__(self):
    return self.name

class Building(models.Model):
  name = models.CharField(max_length=100) 
  slug =models.SlugField(unique=True)

  def __str__(self):
    return self.name



class House(models.Model):
  PAYMENT_CHOICHES=[
    ('كاش','كاش'),
    ('تقسيط','تقسيط')
  ]
  PROPERTY_CHOICHES=[
    ('للبيع','للبيع'),
    ('للأيجار','للأيجار')
    ]
  RENT_CHOICHES=[
    ('سنة','سنة'),
    ('شهر','شهر'),
    ('أسبوع','أسبوع'),
    ('يوم','يوم'),
    ]

  title = models.CharField(max_length=100)
  price = models.IntegerField()
  description =  models.TextField()
  building_type=models.ForeignKey(Building ,on_delete=models.CASCADE)
  flour = models.IntegerField(blank=True, null=True)
  num_rooms =models.IntegerField()
  rent_type =models.CharField(max_length=10,choices=RENT_CHOICHES,blank=True, null=True)
  aria =models.ForeignKey(aria,on_delete=models.SET_NULL ,null=True,related_name='place')
  payment_type =models.CharField(max_length=10,choices=PAYMENT_CHOICHES)
  created = models.DateTimeField(auto_now_add=True)
  space = models.IntegerField()
  slug =models.SlugField(unique=True)
  status =models.BooleanField(default=True)
  cover =models.ImageField(upload_to=uplaod_lucationn)
  property_type =models.CharField(max_length=10,choices=PROPERTY_CHOICHES)
  bathrooms =models.IntegerField()
  Agent =models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)


  def __str__(self):
    return self.title

class extras(models.Model):
  name = models.CharField(max_length=100)
  proper = models.ForeignKey(House,on_delete=models.CASCADE )


class galary(models.Model):
  image = models.ImageField(upload_to=uplaod_lucation)
  proper=models.ForeignKey(House,on_delete=models.CASCADE)


class Contact(models.Model):
  name = models.CharField(max_length=100)
  email = models.EmailField()
  subject = models.CharField(max_length=100)
  messaage =models.TextField()
  
  def __str__(self):
      return self.name
  
