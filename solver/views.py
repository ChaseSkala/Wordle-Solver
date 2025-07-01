import requests

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .objects import WordleData

def index(request):
    template = loader.get_template('solver/wordle.html')
    return HttpResponse(template.render({}, request))

def wordle_solver_view(request):
    url = "https://nw7ncdiil6lcwvxqbko2i65no40tuchx.lambda-url.us-east-2.on.aws/"

    payload = {}
    headers = {}

    try:

        response = requests.get(url)
        data = response.json()
        wordleData2 = WordleData.from_dict(data)
    except requests.exceptions.RequestException as e:
        raise e

    context = {
        "solution": wordleData2.solution,
        "attempts": wordleData2.attempts - 1,
        "guesses": wordleData2.guesses,
    }

    return render(request, "solver/wordle.html", context)
