from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    """ Model for Car Makes
 - Name
 - Description
 - __str__ method to print a car make object
"""
    name = models.CharField(null=False, max_length=30,default="Car Make")

    def __str__(self):
        return "Car Make: "+self.name

class CarModel(models.Model):
    """ Model for Car Model
 - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
 - Name
 - Dealer id, used to refer a dealer created in cloudant database
 - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
 - Year (DateField)
 - Any other fields you would like to include in car model
 - __str__ method to print a car make object"""
    make = models.ForeignKey(CarMake,on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30,default="Car Model")   
    dealer_id =  models.IntegerField()
    SEDAN = "sedan"
    SUV = "suv"
    WAGON = "wagon"

    CAR_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'Sport Utility Vehicle'),
        (WAGON, 'Station Wagon')
    ]
    type = models.CharField(
        null=False, 
        max_length=20, 
        choices=CAR_TYPE_CHOICES, 
        default=SEDAN
    )
    year = models.DateField(null=True)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
