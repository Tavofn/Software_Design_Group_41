from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.forms import inlineformset_factory
from django.contrib import messages
from .models import Order, Customer, Product, FuelQuote
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

@login_required(login_url='login')
@admin_only
def home(request):
    last_five_orders = Order.objects.all().order_by('-date_created')[:5]
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'last_five_orders': last_five_orders,
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }
    return render(request, 'accounts/dashboard.html', context)

def get_quote(request):
    try:
        gallons_requested = float(request.GET.get('gallons', 0))
        state = request.GET.get('state', '')
        has_history = request.GET.get('has_history', 'false').lower() == 'true'

        current_price = 1.50
        location_factor = 0.02 if state == 'Texas' else 0.04
        rate_history_factor = 0.01 if has_history else 0.00
        gallons_requested_factor = 0.02 if gallons_requested > 1000 else 0.03
        company_profit_factor = 0.10

        margin = current_price * (location_factor - rate_history_factor + gallons_requested_factor + company_profit_factor)
        suggested_price = current_price + margin
        total_amount = gallons_requested * suggested_price

        return JsonResponse({
            'suggested_price': round(suggested_price, 2),
            'total_amount': round(total_amount, 2)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def quote_submission(request):
    if request.method == 'POST':
        FuelQuote.objects.create(
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            zip_code=request.POST.get('zip'),
            gallons_requested=request.POST.get('gallons'),
            has_history=request.POST.get('has_history') == 'on',
            suggested_price=request.POST.get('suggested_price'),
            total_amount=request.POST.get('total_amount')
        )
        return redirect('allOrders')
    return render(request, 'order_form.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'customer'])
def display_quotes(request):
    quotes = FuelQuote.objects.all()
    return render(request, 'user.html', {'quotes': quotes})

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    quotes = FuelQuote.objects.all()
    context = {'quotes': quotes}
    return render(request, 'accounts/user.html', context)  # Updated path here

@login_required(login_url='login')
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    return render(request, 'accounts/account_settings.html', {'form': form})

@login_required(login_url='login')
@admin_only # if customer the redirect to user-page and if admin redirect to view_func
def allOrders(request):
    orders = Order.objects.all()
    context = {
        'orders':orders,
    }

    return render(request, 'accounts/all_orders.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) # we can add more like - ['admin', 'staff', etc]
def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products':products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) # we can add more like - ['admin', 'staff', etc]
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()  # order_set means customers child order from model fields
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customer':customer,
        'orders':orders,
        'order_count':order_count,
        'myFilter':myFilter
    }

    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) # we can add more like - ['admin', 'staff', etc]
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=3) # Parent model and Child model. extra=3 means you will see three times form to place order 3 items together. You can use extra=10 or extra=5 as you wish.
    pk = int(pk)
    
    customer = Customer.objects.get(id=str(pk))

    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    # form = OrderForm(initial={'customer':customer}) # To see the customer in form, for which customer profile i viewd.

    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')

    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)




@login_required(login_url='login')
def createOrder_user(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'delivery_address', 'delivery_date','price'),extra=1) # Parent model and Child model. extra=3 means you will see three times form to place order 3 items together. You can use extra=10 or extra=5 as you wish.
    pk = int(pk)
    
    customer = Customer.objects.get(id=str(pk))

    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    # form = OrderForm(initial={'customer':customer}) # To see the customer in form, for which customer profile i viewd.

    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')

    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)





@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) # we can add more like - ['admin', 'staff', etc]
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)

    form = OrderForm(instance=order) # to get pre-field form

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order) # Update (instance) and Post
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'accounts/update_order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) # we can add more like - ['admin', 'staff', etc]
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('home')

    context = {'item':order}
    return render(request, 'accounts/delete.html', context)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()  # Now UserCreationForm will replace by CreateUserForm

    if request.method == 'POST':
        form = CreateUserForm(request.POST)  # Now UserCreationForm will replace by CreateUserForm
        if form.is_valid():
            # user = form.save() # to associated user with group
            username = form.cleaned_data.get('username') # to associated user with group
            messages.success(request, 'Account was created for ' + username) # to associated user with group
            return redirect('login')

    context = {'form':form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password) # to check the user is in model/db or not.
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is Incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)

    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer # logged in user
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)


def get_quote(request):
    # Your calculation logic here
    try:
        gallons_requested = float(request.GET.get('gallons', 0))
        state = request.GET.get('state', '')
        has_history = request.GET.get('has_history', 'false').lower() == 'true'
        
        current_price = 1.50  
        location_factor = 0.02 if state == 'Texas' else 0.04
        rate_history_factor = 0.01 if has_history else 0.00
        gallons_requested_factor = 0.02 if gallons_requested > 1000 else 0.03
        company_profit_factor = 0.10
        
        margin = current_price * (location_factor - rate_history_factor + gallons_requested_factor + company_profit_factor)
        suggested_price = current_price + margin
        total_amount = gallons_requested * suggested_price
        
        return JsonResponse({
            'suggested_price': round(suggested_price, 2),
            'total_amount': round(total_amount, 2)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
def quote_submission(request):
    if request.method == 'POST':
        # Retrieve form data
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')
        gallons_requested = request.POST.get('gallons')
        has_history = request.POST.get('has_history') == 'on'
        suggested_price = request.POST.get('suggested_price')
        total_amount = request.POST.get('total_amount')

        # Create a new FuelQuote instance and save to database
        FuelQuote.objects.create(
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            gallons_requested=gallons_requested,
            has_history=has_history,
            suggested_price=suggested_price,
            total_amount=total_amount
        )
        
        # Redirect to a new URL:
        return redirect('allOrders')  # Replace 'success_url' with the name of the URL to redirect to upon success

    # If not POST, just show the form again
    return render(request, 'order_form.html')