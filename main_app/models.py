from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



# Create your models here.
class Digimon(models.Model):
  name = models.CharField(max_length=250)
  img = models.CharField(max_length=250)
  level = models.TextField(max_length=250)
  happiness = models.IntegerField()
  # Create a cat >--< Toy relationship
  # toys = models.ManyToManyField('Toy')
  # User --< Cat
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  
  def __str__(self):
    return f"{self.name} ({self.id})"
  
  # def fed_for_the_day(self):
  #   return self.feeding_set.filter(date='2025-02-14').count() >= 3
  
  # Define a method to get the URL for this particular cat instance
  def get_absolute_url(self):
    # Use the 'reverse' function to dynamically find URL for 
    #   viewing this cat's details
    return reverse('digimon-detail', kwargs={'digimon_id': self.id })
  
  
# class Feeding(models.Model):
#   date = models.DateField('Feeding date')
#   meal = models.CharField(
#     max_length=1,
#     # add the "choices" field option
#     choices=MEALS,
#     # set default value for meal to be 'B'
#     default=MEALS[0][0]
#     )
 
  '''
  The child in a 1:many relationship must have a ForeignKey that ref's
    the parent object's ID. Because a feeding belogs to a cat, we need
    to add the FreignKey to the Feeding model
  The name 'cat' allos us to access the cat object for any feeding
    object, Ex. the_feeding.cat -> a cat object.
  This allows us to do things such as the_feeding.cat.name to render
    a feeding's cat's name.
    
  However, the column name in the feeding table, is named cat_id, which
    holds the id/PrimaryKey (pk) of the cat object that the feeding
    belongs to.
    
  What about accessing the feeding for a cat? By default, there will
    be an attribute added to a cat object named feeding_set, which is a
    "related (objects) manager", thus we will be able to access a cat's
    feedings like this: at.feeding_set.all() or cat.feeding_set.filter(...)
  If you want to, you can change the name of the related manager by adding a
    related_name kwarg to the ForeignKey, 
    Ex. models.ForeignKey(Cat, on_delete=models.CASCADE, related_name='feedings')
    
  '''
  # cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
  
  # def __str__(self):
  #   # Method for obtaining the friendly value of a Field.choice
  #   return f"{self.get_meal_display()} on {self.date}"
  
  # # Define the default order of feedings
  # class Meta:
  #   ordering = ['date']  # This line makes the newest feedings appear first
    

  