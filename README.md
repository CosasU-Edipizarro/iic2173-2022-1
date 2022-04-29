# Tarea 1

**G19**

## Información de la plataforma

| Campo       | Valor                         |
| ----------- | ----------------------------- |
| IP Servidor | 54.176.117.213                |
| URL         | https://tarea-edipizarro.xyz/ |

## Stack

|            | Lenguaje   | Framework  | Source code                            |
| ---------- | ---------- | ---------- | -------------------------------------- |
| API        | Python     | Django     | `~/backend_django`                     |
| Storage    | SQL        | PostgreSQL | `-`                                    |
| Web server | nginx      | -          | `~/config/nginx/production/local.conf` |

# Instrucciones

1. Hacer builds de frontend y backend
   ```
   sudo docker-compose build
   ```

2. Ejecutar migraciones
   ```
   sudo docker-compose run --rm djangobackend /bin/bash -c "python ./manage.py makemigrations"
   sudo docker-compose run --rm djangobackend /bin/bash -c "python ./manage.py migrate"
   ```

3. Collect statics
   ```
   sudo docker-compose run --rm djangobackend /bin/bash -c "python ./manage.py collectstatic --no-input"
   ```

4. Correr la aplicación
   ```
   sudo docker-compose up
   ```

La APP está disponible en  https://tarea-edipizarro.xyz/

## Comandos útiles

| Comando                                                                                    | Para qué                                          |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| `sudo docker-compose run --rm djangobackend /bin/bash -c "python ./manage.py createsuperuser"` | Crear un admin                                     |
| `sudo docker-compose run --rm djangobackend /bin/bash -c "python ./manage.py {COMMAND}"`       | Ejecutar algun comando del manage.py              |

## Misc
Configuracion/Contraseña de la base de datos: `/config/environment/.env.db`