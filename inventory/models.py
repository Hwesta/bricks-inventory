from django.db import models

# "Reference" tables
class Part(models.Model):
    part_id = models.CharField(max_length=32, unique=True) # lego product code
    name = models.CharField(max_length=256) # descriptive name
    category = models.ForeignKey('Category', to_field='category_id') # eg brick, minifig head
    weight = models.FloatField(null=True, blank=True) 
    x_dimension = models.FloatField(null=True, blank=True)
    y_dimension = models.FloatField(null=True, blank=True)
    z_dimension = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return self.part_id+"-"+self.name

class Category(models.Model):
    # need way to populate this automatically based on what things are referenced
    # in parts initial data
    # NOTE may need split into PartCategory and SetCategory
    category_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return unicode(self.category_id)+"-"+self.name

class Color(models.Model):
    color_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    rgb = models.CharField(max_length=6) # should be hex rgb value
    color_type = models.CharField(max_length=64)
    year_from = models.IntegerField(null=True, blank=True)
    year_to = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return unicode(self.color_id)+"-"+self.name

class PartInstance(models.Model): # existant part in specific color aka Code
    color = models.ForeignKey('Color', to_field='color_id')
    part = models.ForeignKey('Part', to_field='part_id')
#    codename = models.CharField(max_length=255)
    user_override = models.BooleanField(default=False) # for if the user wants to enter something we don't have stored

    def __unicode__(self):
        return unicode(self.part)+" ("+self.color.name+")"
    
class Set(models.Model):
    # TODO stores (PartInstance, number in set) in some form - JSON??
    set_id = models.CharField(max_length=32)
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    
    def __unicode__(self):
        return self.set_id+"-"+self.name

# Actual inventory tables
    
class Inventory(models.Model):
    partinstance = models.ForeignKey('PartInstance')
    count = models.IntegerField()
    location = models.ManyToManyField('Location')
    keywords = models.ManyToManyField('Keyword', through='KeywordValue')
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.count)+"x"+unicode(self.partinstance)

class Location(models.Model):
    name = models.CharField(max_length=256)
    parent = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return self.name;

class Keyword(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

class KeywordValue(models.Model):
    inventory = models.ForeignKey('Inventory')
    keyword = models.ForeignKey('Keyword')
    value = models.CharField(max_length=256)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.inventory+" "+self.keyword+" "+self.value
    



