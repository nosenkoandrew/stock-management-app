from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockCreateForm, StockSearchForm, StockUpdateForm, IssueForm, ReceiveForm
from django.http import HttpResponse
from django.contrib import messages
import csv


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
        queryset = Stock.objects.filter(#category__icontains=form['category'].value(),
                                        item_name__icontains=form['item_name'].value(),
                                        )

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quantity])
            return response

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
        messages.success(request, 'Successfully added')
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
            messages.success(request, 'Successfully updated')
            return redirect('/items_list')

    context = {
        'form': form,
    }
    return render(request, 'stock_management/add_item.html', context)


def delete_item(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Successfully deleted')
        return redirect('/items_list')
    return render(request, 'stock_management/delete_item.html')


def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "queryset": queryset,
    }
    return render(request, "stock_management/detail.html", context)


def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity -= instance.issue_quantity
        messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store")
        instance.save()

        return redirect('/stock_detail/'+str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": 'Issue ' + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }
    return render(request, "stock_management/add_item.html", context)


def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity += instance.receive_quantity
        instance.save()
        messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name)+"s now in Store")

        return redirect('/stock_detail/'+str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())
    context = {
            "title": 'Reaceive ' + str(queryset.item_name),
            "instance": queryset,
            "form": form,
            "username": 'Receive By: ' + str(request.user),
    }
    return render(request, "stock_management/add_item.html", context)
