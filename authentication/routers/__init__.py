from routers import auth, users, chat

routers = {
    "auth": auth.router,
    "users": users.router,
    "chat": chat.router,
}