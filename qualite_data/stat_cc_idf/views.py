#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import Http404
from datetime import datetime
from stat_cc_idf.models import VerifNombreEntites

def date_actuelle(request):
    return render(request, 'date.html', {'date': datetime.now()})
    
def NbEntites(request):
    nbEntites = VerifNombreEntites.objects.all()
    return render(request,'NombreEntites.html',{'nb_ent':nbEntites})
# Create your views here.
