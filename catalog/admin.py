from django.contrib import admin
from .models import Categoria, Ingrediente, Cupcake


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug')
    prepopulated_fields = {'slug': ('nome',)}


@admin.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'alergenico', 'tipoAlergia')
    list_filter = ('alergenico',)


@admin.register(Cupcake)
class CupcakeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sabor', 'preco', 'ativo', 'destaque', 'calorias')
    list_filter = ('ativo', 'destaque', 'categorias')
    list_editable = ('ativo', 'destaque', 'preco')
    filter_horizontal = ('categorias', 'ingredientes')