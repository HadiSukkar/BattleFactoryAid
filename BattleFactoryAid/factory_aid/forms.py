from django import forms
from .models import Pokemon

TYPE_CHOICES = [
    ('None', 'No Type'),
    ('Bug', 'Bug'),
    ('Dark', 'Dark'),
    ('Dragon', 'Dragon'),
    ('Electric', 'Electric'),
    ('Fighting', 'Fighting'),
    ('Fire', 'Fire'),
    ('Flying', 'Flying'),
    ('Ghost', 'Ghost'),
    ('Grass', 'Grass'),
    ('Ground', 'Ground'),
    ('Ice', 'Ice'),
    ('Normal', 'Normal'),
    ('Poison', 'Poison'),
    ('Psychic', 'Psychic'),
    ('Rock', 'Rock'),
    ('Steel', 'Steel'),
    ('Water', 'Water')
]

STYLE_CHOICES = [
    ('0', 'Free Spirited and Unrestrained'),
    ('1', 'Based on Total Preparation'),
    ('2', 'Slow and Steady'),
    ('3', 'One of Endurance'),
    ('4', 'High Risk, High Return'),
    ('5', 'Weakening the Foe to Start'),
    ('6', 'Impossible to Predict'),
    ('7', 'Depend on the Battle\'s Flow'),
    ('8', 'Flexibly Adaptable to the Situation')
]

TIER_CHOICES = [
    ('1', 'Tier 1'),
    ('2', 'Tier 2'),
    ('3', 'Tier 3'),
    ('4', 'Tier 4'),
    ('5', 'Tier 5')
]

pokemon_names = [(name, name) for name in Pokemon.objects.values_list('pokemon', flat=True).distinct().order_by('pokemon')]

class TeamSearchForm(forms.Form):
    type_phrase = forms.ChoiceField(
        label='Type Phrase', 
        choices=TYPE_CHOICES,
        required=False
    )
    style_phrase = forms.ChoiceField(
        label='Style Phrase', 
        choices=STYLE_CHOICES,
        required=False
    )

    pokemon_1 = forms.ChoiceField(choices=pokemon_names, required=False, label='Select Pokémon 1')
    pokemon_2 = forms.ChoiceField(choices=pokemon_names, required=False, label='Select Pokémon 2')
    pokemon_3 = forms.ChoiceField(choices=pokemon_names, required=False, label='Select Pokémon 3')
    pokemon_4 = forms.ChoiceField(choices=pokemon_names, required=False, label='Select Pokémon 4')
    pokemon_5 = forms.ChoiceField(choices=pokemon_names, required=False, label='Select Pokémon 5')
    pokemon_6 = forms.ChoiceField(choices=pokemon_names, required=False, label='Select Pokémon 6')

    tier = forms.ChoiceField(choices=TIER_CHOICES, required=False, label='Tier')
    open_level = forms.BooleanField(required=False, label='Open Level')

    def clean_pokemon_names(self):
        data = self.cleaned_data['pokemon_names']
        pokemon_list = [name.strip() for name in data.split(',')]
        return pokemon_list