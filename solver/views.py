from http.client import HTTPException
from json import JSONDecodeError

import requests
import json

from django.http import HttpResponse, Http404
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

                    if response.status_code == 200:

                        data = response.json()

                        wordleData2 = WordleData.from_dict(data)

                        context = {
                            "solution": wordleData2.solution,
                            "attempts": wordleData2.attempts - 1,
                            "guesses": wordleData2.guesses,
                        }
                        return render(request, 'solver/wordle.html', context)
                    else:
                        context = {
                            "error": response.status_code,
                        }
                        return render(request, "solver/errorscreen.html", context)

                except HTTPException as e:
                    context = {
                        "error": str(e),
                    }
                    return render(request, "solver/errorscreen.html", context)



            else:
                url = "https://nw7ncdiil6lcwvxqbko2i65no40tuchx.lambda-url.us-east-2.on.aws/"

                payload = {}
                headers = {}

                try:

                    response = requests.get(url)

                    if response.status_code == 200:

                        data = response.json()

                        wordleData2 = WordleData.from_dict(data)

                        context = {
                            "solution": wordleData2.solution,
                            "attempts": wordleData2.attempts - 1,
                            "guesses": wordleData2.guesses,
                        }
                        return render(request, 'solver/wordle.html', context)
                    else:

                        context = {
                            "error": response.status_code,
                        }

                        return render(request, "solver/errorscreen.html", context)

                except HTTPException as e:
                    context = {
                        "error": str(e),
                    }
                    return render(request, "solver/errorscreen.html", context)

    return render(request, "solver/form.html")