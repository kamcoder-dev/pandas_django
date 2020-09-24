from django.shortcuts import render
from .models import Purchase, Product
import pandas as pd
from .utils import get_simple_plot
from .forms import PurchaseForm
from django.shortcuts import redirect


def chart_select_view(request):
    graph = None
    error_message = None
    df = None
    price = None

    try:
        product_df = pd.DataFrame(Product.objects.all().values())
        purchase_df = pd.DataFrame(Purchase.objects.all().values())
        product_df['product_id'] = product_df['id']

        if purchase_df.shape[0] > 0:
            df = pd.merge(purchase_df, product_df, on="product_id")
            price = df['price']
            if request.method == 'POST':
                chart_type = request.POST.get('sales')
                date_from = request.POST.get('date_from', '')
                date_to = request.POST.get('date_to', '')
                df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
                df2 = df.groupby('date', as_index=False)[
                    'total_price'].agg('sum')

                if chart_type != "":
                    if date_from != "" and date_to != "":
                        df = df[(df['date'] > date_from)
                                & (df['date'] < date_to)]
                        df2 = df.groupby('date', as_index=False)[
                            'total_price'].agg('sum')
                    graph = get_simple_plot(
                        chart_type, x=df2['date'], y=df2['total_price'], data=df)
                else:
                    error_message = "Please select a chart type to continue on..."

    except:
        product_df = None
        purchase_df = None
        error_message = "No Records in the database"

    return render(request, 'products/main.html', {'error_message': error_message, 'graph': graph, 'price': price, })


def add_purchase_view(request):
    added_message = None
    form = PurchaseForm(request.POST or None)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.salesman = request.user
        obj.save()

        form = PurchaseForm()
        added_message = "The purchase has been added"

    return render(request, 'products/add.html', {'form': form, 'added_message': added_message})
