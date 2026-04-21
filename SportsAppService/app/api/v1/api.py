from fastapi import APIRouter
from app.api.v1.endpoints.SportEndpoint import sport_endpoint
from app.api.v1.endpoints.SportCategoryEndpoint import sport_category_endpoint
from app.api.v1.endpoints.AthleteEndpoint import athlete_endpoint
from app.api.v1.endpoints.LeagueEndpoint import league_endpoint
from app.api.v1.endpoints.PlayerEndpoint import player_endpoint

api_router = APIRouter()

api_router.include_router(sport_endpoint)
api_router.include_router(sport_category_endpoint)
api_router.include_router(athlete_endpoint)
api_router.include_router(league_endpoint)
api_router.include_router(player_endpoint)
