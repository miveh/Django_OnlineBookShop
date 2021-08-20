from django.shortcuts import render, redirect

# Create your views here.
from zahra.form import Add


def add_to(request):
    if request.method == 'POST':
        form = Add(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
    else:
        form = Add()

    return redirect('bookdetail')
