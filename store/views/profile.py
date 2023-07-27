from django.shortcuts import render, redirect
from store.models import Customer


def profile_view(request):
    customer_id = request.session.get('customer')
    if customer_id:
        try:
            customer = Customer.objects.get(pk=customer_id)

            if request.method == 'POST':
                customer.first_name = request.POST.get('first_name')
                customer.last_name = request.POST.get('last_name')
                customer.phone = request.POST.get('phone')
                customer.save()

            return render(request, 'profile.html', {'customer': customer})
        except Customer.DoesNotExist:
            return redirect('login')

    return redirect('login')