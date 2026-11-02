# Librería - Catálogo de libros

Proyecto Django con mantenedores de libros, categorías, editoriales y autores.

## Instalación

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/
   cd libreria-django
   ```

2. Instalar las dependencias y activar el entorno:

   ```bash
   pipenv install -r requirements.txt
   pipenv shell
   ```

3. Copiar `.env.example` como `.env` y agregar una SECRET_KEY:

   ```bash
   copy .env.example .env
   ```

4. Aplicar las migraciones y crear un superusuario:

   ```bash
   py manage.py migrate
   py manage.py createsuperuser
   ```

5. Iniciar el servidor:

   ```bash
   py manage.py runserver
   ```