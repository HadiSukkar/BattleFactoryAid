from django.db import models

class Pokemon(models.Model):
    set_id = models.AutoField(primary_key=True)
    pokemon_id = models.IntegerField()
    type = models.CharField(max_length=100)
    style = models.CharField(max_length=100)
    pokemon = models.CharField(max_length=100)
    pokemon_set = models.CharField(max_length=100)
    item = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.pokemon_set}"

    class Meta:
        managed = False
        db_table = 'factory_data'

class Teams(models.Model):
    type_phrase = models.CharField(max_length=100)
    style_phrase = models.CharField(max_length=100)
    composing_sets = models.CharField(max_length=100)
    composing_pokemon = models.CharField(max_length=100)
    tier = models.CharField(max_length=100, default = "0")

    def __str__(self):
        return f"{self.composing_sets}"

    class Meta:
        db_table = 'factory_teams'