from django.core.management.base import BaseCommand
from collections import defaultdict
from factory_aid.models import Pokemon, Teams


class Command(BaseCommand):
    help = 'Populating teams from existing pokemon sets'

    def handle(self, *args, **kwargs):

        def tier_creation(tier):
            include = "-" + str(tier)
            exclude = include + "0"
            legendary_set = {28, 98, 216, 224, 284, 322, 332, 338, 344, 414, 484}    
            # These pokemon will have numbered sets that don't belong in the same tier as the tier it would correspond to for all other pokemon
            legendary_set = {item + tier for item in legendary_set}
            matching_pokemon = Pokemon.objects.filter(pokemon_set__contains=include)
            matching_pokemon = matching_pokemon.exclude(pokemon_set__contains=exclude)

            res = set(matching_pokemon.values_list('set_id', flat=True))
            res = res - legendary_set

            return res
        
        # Creating the Tiers
        TIER_ONE = tier_creation(1)
        TIER_TWO = tier_creation(2)
        TIER_THREE = tier_creation(3)
        TIER_FOUR = tier_creation(4)
        TIER_FIVE = {33, 34, 103, 104, 289, 290, 327, 328, 419, 420, 489, 
                     490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 
                     500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510}
        # Tier Five doesn't technically exist but this will be a flag indicating open level teams

        factory_data = list(Pokemon.objects.all())
        for i in range(len(factory_data) - 2):
            first_pokemon = factory_data[i]
            self.stdout.write(f'Processing set: {i}', ending='\n')
            self.stdout.flush()
            for j in range(i+1, len(factory_data) - 1):
                second_pokemon = factory_data[j]
                # Enacting Species and Item Clause
                if (first_pokemon.pokemon_id == second_pokemon.pokemon_id or first_pokemon.item == second_pokemon.item):
                    continue
                for k in range(j+1, len(factory_data)):
                    third_pokemon = factory_data[k]
                    # Enacting Species and Item Clause
                    if (first_pokemon.item == third_pokemon.item or second_pokemon.pokemon_id == third_pokemon.pokemon_id or second_pokemon.item == third_pokemon.item):
                        continue

                    # Determining Tier
                    def determine_tier(*pokemons):
                        tier_set = {
                            1: TIER_ONE,
                            2: TIER_TWO,
                            3: TIER_THREE,
                            4: TIER_FOUR
                        }
                        if any(pokemon.set_id in TIER_FIVE for pokemon in pokemons):
                            return 5
                        
                        for tier_number in sorted(tier_set.keys(), reverse = True):
                            if all(pokemon.set_id in tier_set[tier_number] for pokemon in pokemons):
                                return tier_number
                            
                        return 0
                    tier = determine_tier(first_pokemon, second_pokemon, third_pokemon)
                    
                    # Processing the types of each pokemon
                    type_counts = defaultdict(int)
                    for current_pokemon in (first_pokemon, second_pokemon, third_pokemon):
                        types = current_pokemon.type.split(' ')
                        for t in types:
                            type_counts[t] += 1
                    
                    # Determining the most common type for the type phrase
                    dominant_count = 0
                    dominant_type = None
                    for t, count in type_counts.items():
                        if count > dominant_count:
                            dominant_type = t
                            dominant_count += count
                        elif count != 0 and dominant_type and count == dominant_count:
                            dominant_type = None
                    type_phrase = dominant_type if dominant_type else "None"

                    # Organize and concatenate the styles of all 3 pokemon
                    style_overall = ''.join([
                        s for t in (first_pokemon, second_pokemon, third_pokemon)
                        for s in t.style.replace('0','').split()
                    ])

                    # Creating a style phrase from all the styles we see
                    style_bucket = [0]*7
                    for c in style_overall:
                        style_bucket[int(c) - 1] += 1
                    style_phrase = 0
                    count_phrases = 0
                    for i in range(1, len(style_bucket)+1):
                        if (style_bucket[i - 1] > 2 and i < 4) or (style_bucket[i - 1] > 1 and i >= 4):
                            style_phrase = i
                            count_phrases += 1
                        if count_phrases == 3:
                            style_phrase = 8
                            break
                    
                    # Create the Teams instance
                    team = Teams(
                        type_phrase = type_phrase,
                        style_phrase = style_phrase,
                        composing_sets = [t.set_id for t in (first_pokemon, second_pokemon, third_pokemon)],
                        composing_pokemon = [t.pokemon_id for t in (first_pokemon, second_pokemon, third_pokemon)],
                        tier = tier
                    )
                    team.save()
        self.stdout.write(self.style.SUCCESS('Successfully generated teams'))
