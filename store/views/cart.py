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
#  
# repo: https://github.com/juanBindez



from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.product import Products
from django.contrib import messages

class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart', {}).keys())
        products = Products.get_products_by_id(ids)
        return render(request, 'cart.html', {'products': products})

    def post(self, request):
        products_to_delete = request.POST.getlist('delete_item')
        cart = request.session.get('cart', {})

        for product_id in products_to_delete:
            try:
                product = Products.objects.get(id=product_id)
                if str(product_id) in cart:
                    cart.pop(str(product_id))
            except Products.DoesNotExist:
                messages.error(request, f"O produto com ID {product_id} não foi encontrado.")

        request.session['cart'] = cart
        messages.success(request, "Os itens selecionados foram removidos do carrinho com sucesso.")

        return redirect('cart')  # Redireciona de volta para a página do carrinho após a exclusão

