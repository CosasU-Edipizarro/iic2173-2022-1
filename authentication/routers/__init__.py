from routers import auth, users

routers = {
    "auth": auth.router,
    "users": users.router,
}