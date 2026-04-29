from fastapi import APIRouter
from app.api.v1.endpoints.SportEndpoint import sport_endpoint
from app.api.v1.endpoints.ReferenceValueEndpoint import reference_value_endpoint
from app.api.v1.endpoints.ReferenceCategoryEndpoint import reference_category_endpoint
from app.api.v1.endpoints.AthleteEndpoint import athlete_endpoint
from app.api.v1.endpoints.LeagueEndpoint import league_endpoint
from app.api.v1.endpoints.PlayerEndpoint import player_endpoint
from app.api.v1.endpoints.TeamEndpoint import team_endpoint
from app.api.v1.endpoints.PositionEndpoint import position_endpoint

api_router = APIRouter()

api_router.include_router(sport_endpoint)
api_router.include_router(reference_value_endpoint)
api_router.include_router(reference_category_endpoint)
api_router.include_router(athlete_endpoint)
api_router.include_router(league_endpoint)
api_router.include_router(player_endpoint)
api_router.include_router(team_endpoint)
api_router.include_router(position_endpoint)