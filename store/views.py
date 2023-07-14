# this is part of the CommerceCore project.
#
#
# Copyright ©  2023  Juan Bindez  <juanbindez780@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import json

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Cliente
from .models import *



cliente = Cliente
ordem = {'get_car_total': 0, 'get_car_itens': 0, 'shipping': False}
carItens = ordem['get_car_itens']

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/sucesso/')  # Redirecionar para a página de sucesso após o registro
    else:
        form = RegistrationForm()
    return render(request, 'store/cadastro.html', {'form': form})


def home(request):
    return render(request, 'store/main.html')


def store(request):
    try:
        autenticado = request.session['autenticado']
    except:
        autenticado = False
        produtos = Produto.objects.all()
        context = {'produtos': produtos,}
        return render(request, 'store/store.html', context)

    if autenticado:
        clienteId = request.session['cliente']
        cliente = Cliente.objects.get(id=clienteId)
        ordem = Ordem.objects.get(cliente=cliente, completo=False)
        carItens = ordem.get_car_itens

    produtos = Produto.objects.all()
    context = {'produtos': produtos,
               'carItens': carItens, 'autenticado': autenticado, 'cliente': cliente}
    return render(request, 'store/store.html', context)


def add_item(request):

    data = json.loads(request.body)
    produtoId = data['produtoId']

    produto = Produto.objects.get(id=produtoId)
    clienteId = request.session['cliente']
    cliente = Cliente.objects.get(id=clienteId)
    ordem_qs = Ordem.objects.filter(cliente=cliente, completo=False)
    if ordem_qs.exists():
        ordem = ordem_qs[0]
    else:
        ordem = Ordem.objects.create(cliente=cliente, completo=False)
    itens = OrdemItem.objects.filter(ordem=ordem, produto=produto)
    if itens.exists():
        ordemItem = itens[0]
        ordemItem.quantidade = (ordemItem.quantidade + 1)
        ordemItem.save()
    else:
        ordemItem = OrdemItem.objects.create(
            produto=produto, ordem=ordem, quantidade=1)

    messages.success(request, produto.nome + ' foi adicionado com sucesso!')
    return JsonResponse('sucesso', safe=False)


def upd_item(request):

    data = json.loads(request.body)
    produtoId = data['produtoId']
    acao = data['acao']

    clienteId = request.session['cliente']
    cliente = Cliente.objects.get(id=clienteId)
    produto = Produto.objects.get(id=produtoId)
    ordem = Ordem.objects.get(cliente=cliente, completo=False)

    itens = OrdemItem.objects.filter(ordem=ordem, produto=produto)

    for ordemItem in itens:
        if acao == 'add':
            ordemItem.quantidade = (ordemItem.quantidade + 1)
        elif acao == 'del':
            ordemItem.quantidade = (ordemItem.quantidade - 1)
        ordemItem.save()
        if ordemItem.quantidade <= 0:
            ordemItem.delete()

    return JsonResponse('sucesso', safe=False)


def carrinho(request):
    clienteId = request.session['cliente']
    cliente = Cliente.objects.get(id=clienteId)
    ordem = Ordem.objects.get(cliente=cliente, completo=False)
    carItens = ordem.get_car_itens
    if carItens != 0:
        itens = ordem.ordemitem_set.all()

        context = {'carItens': carItens, 'ordem': ordem, 'itens': itens,
                   'autenticado': True, 'cliente': cliente}
        return render(request, 'store/cart.html', context)
    else:
        messages.error(request, 'Não existem pedidos a finalizar!')
        produtos = Produto.objects.all()

        context = {'produtos': produtos,
                   'carItens': carItens, 'autenticado': True, 'cliente': cliente}
        return render(request, 'store/store.html', context)


def checkout(request):

    clienteId = request.session['cliente']
    cliente = Cliente.objects.get(id=clienteId)
    ordem = Ordem.objects.get(cliente=cliente, completo=False)
    itens = ordem.ordemitem_set.all()
    carItens = ordem.get_car_itens

    context = {'itens': itens, 'ordem': ordem,
               'carItens': carItens, 'cliente': cliente}
    return render(request, 'store/checkout.html', context)


def entrar(request):
    return render(request, 'store/login.html')

def user_cadastrado(request):
    return render(request, 'store/sucesso.html')


def login(request):
    try:
        cliente = Cliente.objects.get(email=request.POST['email'])
        existe = True
    except:
        existe = False

    if existe and cliente.check_password(request.POST['senha']):
        request.session['cliente'] = cliente.id
        clienteId = request.session['cliente']
        ordem, created = Ordem.objects.get_or_create(
            cliente=cliente, completo=False)
        itens = ordem.ordemitem_set.all()
        carItens = ordem.get_car_itens
        request.session['autenticado'] = True
        produtos = Produto.objects.all()
        context = {'produtos': produtos,
                   'carItens': carItens, 'autenticado': request.session['autenticado'], 'cliente': cliente}
        return render(request, 'store/store.html', context)
    else:
        items = []
        ordem = {'get_car_total': 0, 'get_car_itens': 0, 'shipping': False}
        carItens = ordem['get_car_itens']
        request.session.clear
        if not existe:
            messages.error(request, 'E-mail não reconhecido!')
        else:
            messages.error(request, 'Senha está incorreta!')

        return render(request, 'store/login.html')


def sair(request):
    logout(request)
    return render(request, 'store/store.html')

