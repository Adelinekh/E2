from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .utils import make_prediction
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import SearchHistory

from django.contrib.auth.decorators import login_required
from .models import SearchHistory
import json
from datetime import datetime
from django.shortcuts import render, HttpResponse
from .utils import make_prediction



def index(request):
    return render(request, 'index.html')


class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'




def predict(request):
    if request.method == 'POST':
        X_predict = {}
        for var in [
                'Year_Built', 'Total_Bsmt_SF', 'Flr_SF', 'Gr_Liv_Area',
                'Garage_Area', 'Overall_Qual', 'Bath', 'Exter_Qual',
                'Kitchen_Qual', 'Neighborhood']:
            var_value = request.POST.get(var)
            if var_value is not None:
                if var in ['Exter_Qual', 'Kitchen_Qual', 'Neighborhood']:
                    X_predict[var] = var_value
                else:
                    X_predict[var] = int(var_value)
        data = request.POST.dict()


        # Calcul de l'âge de la maison
        current_year = datetime.now().year
        year_built = int(X_predict.get('Year_Built', 0))  # Utilisation de get avec une valeur par défaut de 0
        age_house = current_year - year_built
        X_predict['Age_house'] = age_house

        # Calcul de la surface totale
        total_sf = int(X_predict.get('Total_Bsmt_SF', 0)) + int(X_predict.get('Flr_SF', 0))  # Utilisation de get avec une valeur par défaut de 0
        X_predict['Total_SF'] = total_sf

        # Supprimer les clés correspondantes de X_predict
        for key in ['Year_Built', 'Total_Bsmt_SF', 'Flr_SF']:
            del X_predict[key]

        # Effectuer la prédiction
        pred = make_prediction(X_predict)

        # Enregistrer l'historique de recherche
        search_history = SearchHistory.objects.create(
            user=request.user,
            input_variables=data,
            prediction_result=pred
        )
        search_history.save()

        if pred != 0:
            return render(request, 'index.html', {'data': int(pred)})
        else:
            return HttpResponse("The Input is not Correct")
    else:
        return HttpResponse("Method Not Allowed")





@login_required
def search_history(request):
    user = request.user
    search_history = SearchHistory.objects.filter(user=user).order_by('-search_date')
    return render(request, 'search_history.html', {'search_history': search_history})

@login_required
def clear_search(request, search_id):
    search = get_object_or_404(SearchHistory, pk=search_id, user=request.user)
    search.delete()
    return redirect('search_history')