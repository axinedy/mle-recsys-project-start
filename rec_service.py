import logging
from urllib.request import Request

from fastapi import FastAPI
from starlette.responses import JSONResponse

from recommendations import Recommendations
from similar_items import SimilarItems


MAX_K = 100
log = logging.getLogger("uvicorn.error")

rec_store = Recommendations()
rec_store.load(
    "personal",
    'recommendations.parquet',
    columns=["user_id", "item_id", "score", "tracks_total", "hearing_days", "tracks_per_day", "nusers", "rank"],
)
rec_store.load(
    "default",
    'top_popular.parquet',
    columns=["track_id", "users", ],
)

sim_store = SimilarItems()
sim_store.load(
    "similar.parquet",
    columns=["score", "track_id_1", "track_id_2"]
)


app = FastAPI(title="Сервис рекомендаций")


class RangeError(Exception):
    pass


@app.exception_handler(RangeError)
async def value_error_exception_handler(request: Request, exc: RangeError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},)


@app.get(
    "/recommendations",
    summary="Получение", tags=["Рекомендации"],
    description="""
        Возвращает персональные рекомендации для пользователя, при их наличии, иначе рекомендации по умолчанию.
        Если имеется онлайн-история, то, к полученным выше описанным способом рекомендациям, подмешиваются похожие трэки. 
        """)
async def recommendations(user_id: int, k: int = 10):
    if k > MAX_K or k <= 0:
        raise RangeError("k is out of range")
    recs = rec_store.get(user_id, k)
    return {"recs": recs}


def dedup_ids(ids):
    seen = set()
    ids = [id for id in ids if not (id in seen or seen.add(id))]

    return ids


@app.get("/")
def root():
    return "recommendations service"
