from collections import Counter
from django.core.management.base import BaseCommand
from factory_aid.models import Teams, Pokemon
from django.db.models import Q
import pdb
import ast

class Command(BaseCommand):
    help = 'Perform calculations type and style phrases but excludig six Pokemon'

    def add_arguments(self, parser):
        parser.add_argument('type_phrase', type=str, help='Type phrase to include')
        parser.add_argument('style_phrase', type=str, help='Style phrase to include')
        parser.add_argument('pokemon_names', nargs=6, type=str, help='List of six Pokemon names')
    
    def handle(self, *args, **options):
        type_phrase = options['type_phrase']
        style_phrase = options['style_phrase']
        pokemon_names = options['pokemon_names']

        pokemon_ids = Pokemon.objects.filter(pokemon__in=pokemon_names).values_list('pokemon_id', flat=True)

        exclusion_query = Q()
        for pid in pokemon_ids:
            exclusion_query |= Q(composing_pokemon__contains=[pid])

        teams = Teams.objects.filter(
            type_phrase__icontains=type_phrase,
            style_phrase__icontains=style_phrase
        )

        for pid in pokemon_ids:
            teams = teams.exclude(composing_pokemon__contains=pid)

        set_id_counter = Counter({i:0 for i in range(1,511)})
        for team in teams:
            composing_sets = ast.literal_eval(team.composing_sets)
            unique_set_ids = set(composing_sets)
            set_id_counter.update(unique_set_ids)
        
        total_teams=teams.count()
        set_id_percentage = {set_id: (count / total_teams) * 100 for set_id, count in  set_id_counter.items()}

        with open('set_percentages.txt','w') as file:
            for set_id in range(1, 511):
                if set_id in [33, 34, 103, 104, 289, 290, 327, 328, 419, 420, 489, 490] or set_id > 490:
                    continue
                self.stdout.write(f'Set ID {set_id}: {set_id_percentage[set_id]:.2f}%')
                file.write(f'{set_id_percentage[set_id]:.2f}%\n')