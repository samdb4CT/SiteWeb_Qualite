#-*- coding: utf-8 -*-
#!/usr/bin/env python3
from django import forms

class ContactForm(forms.Form):
    host = forms.CharField(max_length=100)
    db_name = forms.CharField(max_length=100)
    user = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    city_context_name = forms.CharField(max_length=100)