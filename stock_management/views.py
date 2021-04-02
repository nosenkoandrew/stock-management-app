from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockCreateForm


def home(request):
    title = 'Home page'
    context = {
        'title': title,
    }
    return render(request, 'stock_management/home.html', context)


def items_list(request):
    title = 'List of items'
    queryset = Stock.objects.all()
    context = {
        'title': title,
        'queryset': queryset
    }
    return render(request, 'stock_management/items_list.html', context)


def add_item(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/items_list')

    context = {
        'form': form,
        'title': "Add title",
    }
    return render(request, 'stock_management/add_item.html', context)