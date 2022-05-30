from routers import auth, locations, users, pings, protected, count, externalapi

routers = {
    "auth": auth.router,
    "locations": locations.router,
    "users": users.router,
    "pings": pings.router,
    "protected": protected.router,
    "count": count.router,
    "externalapi": externalapi.router
}