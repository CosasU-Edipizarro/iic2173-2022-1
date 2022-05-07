from routers import auth, locations, users, protected

routers = { 
    "auth": auth.router,
    "locations": locations.router,
    "users": users.router,
    "protected": protected.router,
}