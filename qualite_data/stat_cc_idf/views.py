#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import Http404
from datetime import datetime
import django_tables2 as tables
from django_tables2 import RequestConfig
from stat_cc_idf.models import VerifNombreEntites

def date_actuelle(request):
    return render(request, 'date.html', {'date': datetime.now()})
    
def NbEntites(request):
    nbEntites = VerifNombreEntites.objects.all()
    table = EntiteTable(VerifNombreEntites.objects.all())
    table.paginate(page=request.GET.get('page', 1), per_page=500)
    RequestConfig(request,paginate={'per_page': 500}).configure(table)
    return render(request,'NombreEntites.html',{'nb_ent':table})
# Create your views here.

class EntiteTable(tables.Table):
    class Meta:
        model = VerifNombreEntites
        attrs = {'class': 'palegreen'}
        
