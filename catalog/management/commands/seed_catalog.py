from django.core.management.base import BaseCommand
from catalog.models import Categoria, Ingrediente, Cupcake


CATEGORIAS = [
    ('Tradicional', 'Cupcakes clássicos'),
    ('Vegano', 'Sem ingredientes de origem animal'),
    ('Diet', 'Sem açúcar e baixa caloria'),
    ('Especial', 'Sabores sazonais e edições limitadas'),
]

INGREDIENTES = [
    ('Farinha de trigo', False, ''),
    ('Açúcar', False, ''),
    ('Ovo', True, 'Ovo'),
    ('Leite', True, 'Lactose'),
    ('Chocolate', False, ''),
    ('Amendoim', True, 'Amendoim'),
    ('Morango', False, ''),
    ('Baunilha', False, ''),
    ('Cenoura', False, ''),
    ('Castanha', True, 'Castanha'),
]

CUPCAKES = [
    # nome, sabor, massa, recheio, cobertura, calorias, preco, categoria, ingredientes, destaque
    ('Cupcake de Chocolate', 'Chocolate', 'Chocolate', 'Ganache', 'Chantilly', 320, '12.90', 'Tradicional', ['Farinha de trigo','Açúcar','Ovo','Leite','Chocolate'], True),
    ('Cupcake de Morango', 'Morango', 'Baunilha', 'Geleia de morango', 'Chantilly', 280, '11.50', 'Tradicional', ['Farinha de trigo','Açúcar','Ovo','Leite','Morango'], True),
    ('Cupcake de Cenoura', 'Cenoura', 'Cenoura', 'Doce de leite', 'Chocolate', 300, '12.00', 'Tradicional', ['Farinha de trigo','Açúcar','Ovo','Leite','Cenoura','Chocolate'], False),
    ('Cupcake Vegano de Baunilha', 'Baunilha', 'Vegetal', '', 'Creme de castanha', 250, '14.50', 'Vegano', ['Farinha de trigo','Açúcar','Castanha','Baunilha'], True),
    ('Cupcake Diet de Morango', 'Morango', 'Integral', 'Geleia sem açúcar', 'Iogurte natural', 180, '13.90', 'Diet', ['Farinha de trigo','Morango'], False),
    ('Cupcake Especial de Amendoim', 'Amendoim', 'Chocolate', 'Pasta de amendoim', 'Chocolate', 350, '15.50', 'Especial', ['Farinha de trigo','Açúcar','Ovo','Leite','Chocolate','Amendoim'], True),
]


class Command(BaseCommand):
    help = 'Popula o catálogo com dados de exemplo'

    def handle(self, *args, **kwargs):
        # Categorias
        cat_map = {}
        for nome, desc in CATEGORIAS:
            slug = nome.lower().replace(' ', '-')
            cat, _ = Categoria.objects.get_or_create(
                nome=nome, defaults={'descricao': desc, 'slug': slug}
            )
            cat_map[nome] = cat
        self.stdout.write(self.style.SUCCESS(f'{len(cat_map)} categorias OK'))

        # Ingredientes
        ing_map = {}
        for nome, alerg, tipo in INGREDIENTES:
            ing, _ = Ingrediente.objects.get_or_create(
                nome=nome, defaults={'alergenico': alerg, 'tipoAlergia': tipo}
            )
            ing_map[nome] = ing
        self.stdout.write(self.style.SUCCESS(f'{len(ing_map)} ingredientes OK'))

        # Cupcakes
        count = 0
        for (nome, sabor, massa, recheio, cobertura, calorias, preco,
             cat_nome, ing_nomes, destaque) in CUPCAKES:
            cupcake, created = Cupcake.objects.get_or_create(
                nome=nome,
                defaults={
                    'descricao': f'Delicioso cupcake de {sabor.lower()}.',
                    'preco': preco,
                    'sabor': sabor,
                    'massa': massa,
                    'recheio': recheio,
                    'cobertura': cobertura,
                    'calorias': calorias,
                    'ativo': True,
                    'destaque': destaque,
                }
            )
            if created:
                cupcake.categorias.add(cat_map[cat_nome])
                cupcake.ingredientes.set([ing_map[n] for n in ing_nomes])
                count += 1
        self.stdout.write(self.style.SUCCESS(f'{count} cupcakes criados'))