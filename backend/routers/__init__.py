from routers import auth, locations, users, protected, emails

routers = { 
    "auth": auth.router,
    "locations": locations.router,
    "users": users.router,
    "protected": protected.router,
    "emails": emails.router,
}