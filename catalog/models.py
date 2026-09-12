import uuid
from django.db import models


class Categoria(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Ingrediente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100, unique=True)
    alergenico = models.BooleanField(default=False)
    tipoAlergia = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Ingrediente'
        verbose_name_plural = 'Ingredientes'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Produto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=150)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    imagemUrl = models.ImageField(upload_to='cupcakes/', blank=True, null=True)
    ativo = models.BooleanField(default=True)
    destaque = models.BooleanField(default=False)
    categorias = models.ManyToManyField(Categoria, related_name='produtos')
    ingredientes = models.ManyToManyField(Ingrediente, related_name='produtos', blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-destaque', 'nome']

    def __str__(self):
        return self.nome


class Cupcake(Produto):
    sabor = models.CharField(max_length=100)
    massa = models.CharField(max_length=100)
    recheio = models.CharField(max_length=100, blank=True)
    cobertura = models.CharField(max_length=100, blank=True)
    calorias = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Cupcake'
        verbose_name_plural = 'Cupcakes'

    def __str__(self):
        return f'{self.nome} ({self.sabor})'
