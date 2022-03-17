from django.db import models
from django.conf import settings



class User(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=12)
    password = models.CharField(max_length=200)

    def __str__(self):
      return self.firstname
    

class Labellized_Images(models.Model):
    label = models.CharField(max_length=20)
    image = models.ImageField(upload_to='images',null=False, blank=False)
    ml_name = models.ForeignKey('MLalgorithm', on_delete=models.CASCADE, null =False)

    def __str__(self):
      return str(self.image)

class MLalgorithm(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    algo = models.BinaryField(max_length=None, null=True, blank=True)

    def __str__(self):
      return str(self.name)


    

#comment je fais ici, le mieux c'est si je fais en sorte de mettre le modèle de ML dans la classe MLalgorithm