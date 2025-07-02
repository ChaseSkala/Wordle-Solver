import requests
import json

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .objects import WordleData
from .forms import *

def index(request):
    template = loader.get_template('solver/wordle.html')
    return HttpResponse(template.render({}, request))

def wordle_solver(request):
    if request.method == "POST":
        form = WordleSolverForm(request.POST)
        if form.is_valid():
            guess = form.cleaned_data['guess']

            if guess:
                url = "https://nw7ncdiil6lcwvxqbko2i65no40tuchx.lambda-url.us-east-2.on.aws/guess"

                payload = json.dumps({
                    "guess": f"{guess}",
                })
                headers = {
                    'Content-Type': 'application/json'
                }

                try:

                    response = requests.request("POST", url, headers=headers, data=payload)
                    data = response.json()
                    wordleData2 = WordleData.from_dict(data)


                    context = {
                        "solution": wordleData2.solution,
                        "attempts": wordleData2.attempts - 1,
                        "guesses": wordleData2.guesses,
                    }
                except requests.exceptions.JSONDecodeError:
                    context = {
                        "solution": "ERROR, TRY AGAIN",
                        "attempts": "ERROR, TRY AGAIN",
                        "guesses": "ERROR, TRY AGAIN",
                    }



            else:
                url = "https://nw7ncdiil6lcwvxqbko2i65no40tuchx.lambda-url.us-east-2.on.aws/"

                payload = {}
                headers = {}

                try:

                    response = requests.get(url)
                    data = response.json()
                    wordleData2 = WordleData.from_dict(data)

                    context = {
                        "solution": wordleData2.solution,
                        "attempts": wordleData2.attempts - 1,
                        "guesses": wordleData2.guesses,
                    }
                except requests.exceptions.JSONDecodeError:
                    context = {
                        "solution": "ERROR, TRY AGAIN",
                        "attempts": "ERROR, TRY AGAIN",
                        "guesses": "ERROR, TRY AGAIN",
                    }



            return render(request, "solver/wordle.html", context)
    return render(request, "solver/form.html")