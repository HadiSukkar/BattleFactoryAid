from django.shortcuts import render
from .forms import TeamSearchForm
from .utils import calculate_set_percentages


def teams_search_view(request):
    if request.method == 'POST':
        form = TeamSearchForm(request.POST)
        if form.is_valid():

            type_phrase = form.cleaned_data['type_phrase']
            style_phrase = form.cleaned_data['style_phrase']
            pokemon_names = [form.cleaned_data.get(f'pokemon_{i+1}') for i in range(6)]
            tier = form.cleaned_data['tier']
            open_level = form.cleaned_data['open_level']

            set_percentages, top_sets = calculate_set_percentages(type_phrase, style_phrase, pokemon_names, tier, open_level)

            with open('set_percentages.txt', 'w') as file:
                for set_id in range(1, 511):
                    if set_id in [33, 34, 103, 104, 289, 290, 327, 328, 419, 420, 489, 490] or set_id > 490:
                        continue
                    percentage = set_percentages.get(set_id, 0)
                    file.write(f'{percentage:.2f}%\n')

            context = {
                'form': form,
                'top_sets': top_sets
            }
            return render(request, 'team_results.html', context)
    else:
        form = TeamSearchForm()

    return render(request, 'team_search.html', {'form': form})

