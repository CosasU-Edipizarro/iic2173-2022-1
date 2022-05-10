El diagrama tiene dos componentes principales que son partes de servicios de AWS, uno siendo el backend, el cual esta representando por un componente que viene del servicio EC2, y el frontend que esta representando por un componente que viene del servicio S3.

El cliente se conecta al servidor frontend, el cual luego pasa por una API Gateway (de AWS) y reverse proxy (Nginx) para conectarse al backend.

En cuanto al backend, la mayoría de las funcionalidades provienen de los routers, los cuales se encargan de procesar las requests. Para iniciar sesión, el backend utiliza tokens para autenticar la identidad del usuario y conservar la sesión. Además, el backend tiene una base de datos PostgreSQL extendida para Postgis para el manejo de puntos geograficos. Por otra parte, el manejo de confirmación de correo tambien esta implementado aquí.

El frontend tiene componentes de mapas (de Leaflet) para el manejo de ubicaciones geograficas, a modo de facilitar la forma de añadir lugares.

