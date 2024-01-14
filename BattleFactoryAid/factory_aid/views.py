from django.shortcuts import render
from .forms import TeamSearchForm, PokemonSearchForm
from .utils import calculate_set_percentages, calculate_pokemon_search


def teams_search_view(request):
    search_form = TeamSearchForm(request.POST)
    pokemon_search_form = PokemonSearchForm(request.POST)

    pokemon_search_results = None
    top_sets = request.session.get('top_sets')
    set_percentages = request.session.get('set_percentages')

    if 'team_search' in request.POST and search_form.is_valid():
        type_phrase = search_form.cleaned_data['type_phrase']
        style_phrase = search_form.cleaned_data['style_phrase']
        pokemon_names = [search_form.cleaned_data.get(f'pokemon_{i+1}') for i in range(6)]
        included_pokemon = [search_form.cleaned_data.get(f'included_pokemon_{i+1}') for i in range(3)]
        tier = search_form.cleaned_data['tier']
        open_level = search_form.cleaned_data['open_level']

        set_percentages, top_sets = calculate_set_percentages(type_phrase, style_phrase, pokemon_names, tier, open_level, included_pokemon)

        '''with open('set_percentages.txt', 'w') as file:
            for set_id in range(1, 511):
                if set_id in [33, 34, 103, 104, 289, 290, 327, 328, 419, 420, 489, 490] or set_id > 490:
                    continue
                percentage = set_percentages.get(set_id, 0)
                file.write(f'{percentage:.2f}%\n')'''
        
        request.session['set_percentages'] = set_percentages
        request.session['top_sets'] = top_sets
        request.session['team_search_data'] = search_form.cleaned_data

    elif 'pokemon_search' in request.POST and pokemon_search_form.is_valid():
        team_search_data = request.session.get('team_search_data')
        if team_search_data:
            search_form = TeamSearchForm(initial=team_search_data)
        pokemon_name = pokemon_search_form.cleaned_data['pokemon_name']
        pokemon_search_results = calculate_pokemon_search(pokemon_name, set_percentages)

    context = {
        'search_form': search_form,
        'pokemon_search_form': pokemon_search_form,
        'top_sets': top_sets,
        'pokemon_search_results': pokemon_search_results
    }
    return render(request, 'team_search.html', context)
