from routers import auth, locations, users, pings, protected, emails, count, externalapi

routers = {
    "auth": auth.router,
    "locations": locations.router,
    "users": users.router,
    "pings": pings.router,
    "protected": protected.router,
    "emails": emails.router,
    "count": count.router,
    "externalapi": externalapi.router
}