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



from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    ENUM_GENERO = [
        ('M', 'Masculino'),
        ('F', 'Feminino')
    ]
    nome = models.CharField(max_length=200)
    senha = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    genero = models.CharField(choices=ENUM_GENERO, max_length=1, default='M')
    endereco = models.CharField(max_length=200, null=True, blank=True)
    referencia = models.CharField(max_length=200, null=True, blank=True)
    cidade = models.CharField(max_length=200, default='Brasília')
    telefone = models.CharField(max_length=200, null=True, blank=True)
    autenticado = models.BooleanField(default=False)

    def __str__(self):
        return self.nome + " (" + str(self.id) + ")"

    @property
    def adjetivo(self):
        if self.genero == 'M':
            return 'o'
        return 'a'


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)
    detalhes = models.TextField(null=True, blank=True)
    preco = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        foto = ''
        try:
            foto = self.image.url
        except:
            foto = ''

        return self.nome + " (" + foto + ")"

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Ordem(models.Model):
    cliente = models.ForeignKey(
        Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    dataHora = models.DateTimeField(auto_now_add=True)
    completo = models.BooleanField(default=False)
    transacao_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_car_total(self):
        ordemitens = self.ordemitem_set.all()
        total = sum([item.get_total for item in ordemitens])
        return total

    @property
    def get_car_itens(self):
        ordemitens = self.ordemitem_set.all()
        total = sum([item.quantidade for item in ordemitens])
        return total


class OrdemItem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True)
    ordem = models.ForeignKey(Ordem, on_delete=models.SET_NULL, null=True)
    quantidade = models.IntegerField(default=0, null=True, blank=True)
    dataHora = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.produto.preco * self.quantidade
        return total


class EnderecoEntrega(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    ordem = models.ForeignKey(Ordem, on_delete=models.SET_NULL, null=True)
    endereco = models.CharField(max_length=200, null=False)
    referencia = models.CharField(max_length=200, null=False)
    cidade = models.CharField(max_length=200, null=False)
    dataHora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.endereco
