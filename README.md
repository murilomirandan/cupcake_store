# 🧁 Cupcakes Gourmet — Loja Virtual

Aplicativo de venda online de cupcakes gourmet desenvolvido em **Django** como Projeto Integrador Transdisciplinar em Engenharia de Software II.

## 📋 Funcionalidades

- Vitrine virtual com filtro por categoria e busca
- Detalhes do produto com ingredientes e alergênicos
- Carrinho de compras
- Checkout com endereço de entrega
- Pagamento via Cartão e PIX
- Acompanhamento de pedidos
- Avaliação de experiência
- Painel administrativo completo

## 🛠️ Tecnologias

- Python 3.11+
- Django 5.0
- Bootstrap 5
- SQLite (dev) / PostgreSQL (prod)

## 🚀 Como executar

```bash
# 1. Clonar o repositório
git clone https://github.com/seu-usuario/cupcake-store.git
cd cupcake-store

# 2. Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\Activate.ps1  # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
cp .env.example .env
# Edite o .env com sua SECRET_KEY

# 5. Aplicar migrations
python manage.py migrate

# 6. Criar superusuário
python manage.py createsuperuser

# 7. Rodar o servidor
python manage.py runserver
```

Acesse: http://127.0.0.1:8000

## 📁 Estrutura

```
cupcake_store/
├── accounts/      # Usuário, Cliente, Administrador
├── catalog/       # Cupcake, Categoria, Ingrediente
├── cart/          # Carrinho de compras
├── orders/        # Pedidos
├── payments/      # Pagamentos (Cartão/PIX)
├── delivery/      # Entrega
├── notifications/ # Notificações
├── reviews/       # Avaliações
└── templates/     # Templates HTML
```