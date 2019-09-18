# MyFinances

## Como usar o projeto local
1. Clone o projeto:
```bash
git clone https://github.com/CleitonDeLima/myfinances.git
```

2. Crie um ambiente virtual do python:
```bash
cd myfinances
python -m venv .venv
source .venv/bin/activate
```

3. Crie o arquivo `.env` na raiz do projeto com o conteúdo:
```text
SECRET_KEY=IS_SECRET
DEBUG=True
ALLOWED_HOSTS=*
DATABASE_URL=sqlite3:///db.sqlite3
IS_SECURE=False
```

4. Instale as dependencias:
```bash
pip install -r requirements.txt && pip install ipython
```

5. Rode as migrações:
```bash
python manage.py migrate
```

6. Crie um superuser:
```bash
python manage.py createsuperuser
```

7. Rodar o runserver:
```bash
python manage.py runserver
```
