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



from django.urls import path
from . import views
from .views import register

urlpatterns = [
    # Leave as empty string for base url
    path('', views.home, name='home'),
    path('store', views.store, name='store'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('checkout/', views.checkout, name='checkout'),
    path('entrar/', views.entrar, name='entrar'),
    path('cadastrar/', register, name='registro'),
    path('login/', views.login, name='login'),
    path('add-item/', views.add_item, name='add_item'),
    path('upd-item/', views.upd_item, name='upd_item'),
    path('sair/', views.sair, name='sair'),
]
