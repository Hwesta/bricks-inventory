from django.db import models

# "Reference" tables
class Part(models.Model):
    id = models.CharField(max_length=32) # lego product code, TODO check this doesn't conflict with Django stuff
    name = models.CharField(max_length=256) # descriptive name
    category = models.ForeignKey('Category') # eg brick, minifig head

class Category(models.Model):
    # need way to populate this automatically based on what things are referenced
    # in parts initial data
    # NOTE may need split into PartCategory and SetCategory
    name = models.CharField(max_length=200)

class Color(models.Model):
    name = models.CharField(max_length=200)
    rgb = models.IntegerField() # should be hex rgb value
    color_type = models.CharField(max_length=64)
    year_from = models.IntegerField()
    year_to = models.IntegerField()

class PartInstance(models.Model): # existant part in specific color aka Code
    color = models.ForeignKey('Color')
    part = models.ForeignKey('Part')
    user_override = models.BooleanField(default=False) # for if the user wants to enter something we don't have stored
    
class Set(models.Model):
    # TODO stores (PartInstance, number in set) in some form - JSON??
    id = models.CharField(max_length=32) # TODO check this doesn't conflict with Django stuff
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    

# Actual inventory tables
    
class Inventory(models.Model):
    partinstance = models.ForeignKey('PartInstance')
    count = models.IntegerField()
    location = models.ManyToManyField('Location')
    keywords = models.ManyToManyField('Keyword', through='KeywordValue')
    deleted = models.BooleanField(default=False)

class Location(models.Model):
    pass

class Keyword(models.Model):
    name = models.CharField(max_length=256)

class KeywordValue(models.Model):
    value = models.CharField(max_length=256)
    deleted = models.BooleanField(default=False)
    



