# Tarea 1

**G19**

## Información de la plataforma

| Campo              | Valor                            |
| ------------------ | -------------------------------- |
| IP API             | 3.136.190.174                    |
| URL API GATEWAY    | https://api.iic2173-g19.xyz/     |
| URL FRONT          | https://iic2173-g19.xyz/         |
| Docs API           | https://api.iic2173-g19.xyz/docs |

## Stack

|                | Tech       | Framework  | Source code                            |
| -------------- | ---------- | ---------- | -------------------------------------- |
| API            | Python     | FastAPI    | `~/backend`                            |
| API DB         | SQL        | Postgis    | `-`                                    |
| API Web server | nginx      | -          | `~/config/nginx/production/local.conf` |
| Front          | Javascript | Vue        | `~/frontend`                           |
| Front CDN      | Cloudfront | -          | `AWS`                                  |

## Instrucciones

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

## CI/CD

1. Backend
  El backend tiene CI/CD implementado con Github Actions, Docker, ssh y EC2.
  Solo se ejecuta cuando se hace merge a `master`

2. Frontend
  El backend tiene CI/CD implementado con Github Actions, Yarn, AWS-CLI y S3.
  Solo se ejecuta cuando se hace merge a `master`
  
Para replicar el pipe CI/CD se tienen que copiar los achivos que se encuentran en la carpeta .github/workflows, además se tienen que configurar los actions secrets.

## Comandos útiles
1. Si tienes error 
  ```
  failed to solve with frontend dockerfile.v0
  ```
  En `docker-compose build`
  Correr con sudo
  De seguir persistiendo el error, desactivart Buildkit
  ```
  export DOCKER_BUILDKIT=0
  ```

2. Para que docker corra en boot (Crear systemd service)
  ```
  sudo systemctl enable docker
  sudo systemctl daemon-reload
  sudo systemctl restart docker
  ```

3. Si quieres reinicar TODO docker:
  ```
  sudo docker-compose down
  sudo docker rm -f $(sudo docker ps -a -q)
  sudo docker volume rm $(sudo docker volume ls -q)
  sudo docker image rm $(sudo docker image ls)
  sudo docker-compose up -d
  ```

4. Si instalaste docker compose v2 (Nuevo default), instala compose switch para conseguir compatibilidad con v1 (Usada por archivo `./init-letsencrypt.sh`)
  ```
  https://github.com/docker/compose-switch
  ```

## Misc
Variables de ambiente: `/config/environment/`
Configuración Nginx: `/config/nginx/`
Certificados certbot `/config/certbot/`


## Consideraciones generales
 * Una vez que te logeas, no puedes cerrar sesión por las cookies, mejor probar con ventanas en incognito.
 * Es posible ingresar con un usuario que no existe (pero las cosas no funcionan).
 * El formato de ubicación tiene que ser *latitud, longitud* , sino no se agrega bien la ubicacion.
 * Si un usuario no tiene ubicaciones, se le pondra una por default en la UC.
 * El perfil no es funcional todavia.
 * Por ahora solo se pueden enviar pings y ver cuales te han enviado, pero no se pueden aceptar o rechazar.
 * La documentación del diagrama UML se encuentra dentro de la carpeta /docs
 * La API externa que implementamos agrega la dirección a un lugar según las coordenadas, en "Tus Lugares".

