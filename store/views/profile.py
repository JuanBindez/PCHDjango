from django.shortcuts import render, redirect
from store.models import Customer


'''
def edit_customer(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        customer = Customer.objects.get(pk=customer_id)

        customer.first_name = request.POST.get('first_name')
        customer.last_name = request.POST.get('last_name')
        customer.phone = request.POST.get('phone')
        
        # Salva as alterações no banco de dados
        customer.save()
        
        return redirect('customer_detail', customer_id=customer.id)
    else:
        customer_id = request.GET.get('customer_id')
        customer = Customer.objects.get(pk=customer_id)
        return render(request, 'profile.html', {'customer': customer})
'''  


'''
def profile_view(request):
    customer_id = request.session.get('customer')
    if customer_id:
        try:
            customer = Customer.objects.get(pk=customer_id)
            return render(request, 'profile.html', {'customer': customer})
        except Customer.DoesNotExist:
            # O cliente não foi encontrado no banco de dados, então o ID não é válido
            return redirect('login')  # Redireciona para a página de login

    return redirect('login')  # Redireciona para a página de login caso o

'''


def profile_view(request):
    customer_id = request.session.get('customer')
    if customer_id:
        try:
            customer = Customer.objects.get(pk=customer_id)

            if request.method == 'POST':
                # Tratar a submissão do formulário de edição do perfil
                customer.first_name = request.POST.get('first_name')
                customer.last_name = request.POST.get('last_name')
                customer.phone = request.POST.get('phone')
                customer.save()

            return render(request, 'profile.html', {'customer': customer})
        except Customer.DoesNotExist:
            # O cliente não foi encontrado no banco de dados, então o ID não é válido
            return redirect('login')  # Redireciona para a página de login

    return redirect('login')  # Redireciona para a página de login caso o cl