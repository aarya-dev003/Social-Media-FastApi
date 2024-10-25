from fastapi import FastAPI
from .import models
from .database import engine
from .routers import post, users, auth, vote
from .middleware import add_cors_middleware


#database using sqlalchemy no longer needed because of alembic
# models.Base.metadata.create_all(bind=engine)


app = FastAPI() 

#allowed cors origins
add_cors_middleware(app)

@app.get('/')
async def root():
    return {"message" : "Hello"}


app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

