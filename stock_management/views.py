from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockCreateForm, StockSearchForm, StockUpdateForm


def home(request):
    title = 'Home page'
    context = {
        'title': title,
    }
    return render(request, 'stock_management/home.html', context)


def items_list(request):
    header = 'List of items'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {
        'header': header,
        'queryset': queryset,
        'form': form,
    }
    if request.method == 'POST':
        queryset = Stock.objects.filter(category__icontains=form['category'].value(),
                                        item_name__icontains=form['item_name'].value())
        context = {
            'header': header,
            'queryset': queryset,
            'form': form,
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


def update_item(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)

    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            return redirect('/items_list')

    context = {
        'form': form,
    }
    return render(request, 'stock_management/add_item.html', context)


def delete_item(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        return redirect('/items_list')
    return render (request, 'stock_management/delete_item.html')
