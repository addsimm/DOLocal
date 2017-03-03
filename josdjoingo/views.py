from django.shortcuts import render
from django.template.response import TemplateResponse

import random

from .models import JoingoCard

# Create your views here.

def generate_card_entries():
    entries = []
    for letter in 'BINGO':
        for row in range(1, 60, 15):
            column = list(range(15))
            random.shuffle(column)
            column = column[-5:]
            column = column * row
            entries.append(column)

    return entries


def djoingo_main(request):
    """
    Main Djoingo View
    """
    template = "josdjoingo/djoingo_main.html"
    card = JoingoCard()
    # card.entries = generate_card_entries()
    card.card_serial = 123

    card.entries= [1, 2, 3, 4]
    card.tags =[1,2,3,4]
    card.tags.insert(0, 0)
    typecard = type(card.tags)
    card.save()
    context = {"card": card}

    return TemplateResponse(request, template, context)


