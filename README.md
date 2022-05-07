# Tarea 1

**G19**

## Información de la plataforma

| Campo       | Valor                         |
| ----------- | ----------------------------- |
| IP Servidor | 3.136.190.174                 |
| URL API     | https://api.iic2173-g19.xyz/  |
| URL FRONT   | https://iic2173-g19.xyz/      |

## Stack

|            | Lenguaje   | Framework  | Source code                            |
| ---------- | ---------- | ---------- | -------------------------------------- |
| API        | Python     | FastAPI     | `~/backend`                           |
| Storage    | SQL        | PostgreSQL | `-`                                    |
| Web server | nginx      | -          | `~/config/nginx/production/local.conf` |
| Front      | Javascript | Vue        | `~/frontend`                           |

# Instrucciones

1. Para correr en local
   ```
   docker-compose -f docker-compose.dev.yml build
   docker-compose -f docker-compose.dev.yml up
   ```

2. Para correr en servidor
   ```
   sudo docker-compose build
   sudo docker-compose up -d
   ```

La API está disponible en  https://api.iic2173-g19.xyz/
El frontend está disponible en https://iic2173-g19.xyz/

## Comandos útiles
1. Si tienes error `failed to solve with frontend dockerfile.v0` en `docker-compose build`
   Correr con sudo
   O, de no funcionar sudo
   ```
   export DOCKER_BUILDKIT=0
   ```

2. Si quieres reinicar TODO docker:
   ```
   docker-compose down
   docker rm -f $(docker ps -a -q)
   docker volume rm $(docker volume ls -q)
   docker-compose up -d
   ```

3. Si instalaste docker compose v2, instala compose switch para conseguir compatibilidad con v2
   ```
   https://github.com/docker/compose-switch
   ```

## Misc
Variables de ambiente: `/config/environment/`
Configuración Nginx: `/config/nginx/`
Certificados certbot `/config/certbot/`