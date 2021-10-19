from django.contrib import admin
from .models import CarMake, CarModel
# from .models import related models


# Register your models here.

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    inlines = []
    list_display = ['name',"make","type","dealer_id"]


# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['name']


# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)