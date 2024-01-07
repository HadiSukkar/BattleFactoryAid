from .models import Pokemon, Teams
from django.db.models import Q
from collections import Counter
import ast

def calculate_set_percentages(type_phrase, style_phrase, pokemon_names, tier, open_level):
    pokemon_ids = Pokemon.objects.filter(pokemon__in=pokemon_names).values_list('pokemon_id', flat=True)

    exclusion_query = Q()
    for pid in pokemon_ids:
        exclusion_query |= Q(composing_pokemon__contains=pid)

    teams = Teams.objects.filter(
        type_phrase__icontains=type_phrase,
        style_phrase__icontains=style_phrase
    ).exclude(exclusion_query)

    if tier in ['1', '2', '3', '4']:
        teams = teams.filter(tier=tier)
    elif tier == '5' and not open_level:
        teams = teams.exclude(tier='5')

    set_id_counter = Counter()
    for team in teams:
        composing_sets = ast.literal_eval(team.composing_sets)
        unique_set_ids = set(composing_sets)
        set_id_counter.update(unique_set_ids)

    total_teams = teams.count()
    set_id_percentage = {set_id: round((count / total_teams) * 100,2) for set_id, count in set_id_counter.items()}
    top_set_ids = sorted(set_id_percentage.items(), key=lambda x: x[1], reverse=True)[:10]

    top_sets = [(set_id, Pokemon.objects.get(set_id=set_id).pokemon_set, percentage) for set_id, percentage in top_set_ids]

    # Return the results
    return set_id_percentage, top_sets