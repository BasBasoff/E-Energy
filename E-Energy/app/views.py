"""
Definition of views.
"""
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest

from .models import EntranceMeasure

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    measures = EntranceMeasure.objects.all()
    measures_json = json.dumps(list(measures), cls=DjangoJSONEncoder, default=str)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'values':measures_json
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
