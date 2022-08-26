# Copyright 2022 Marin Pejcin


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.routers import player, team, game

api = FastAPI()

api.include_router(player.router)
api.include_router(team.router)
api.include_router(game.router)

origins = ["*"]

api.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"]
)


@api.get("/")
async def root():
    return {"status": "working"}
