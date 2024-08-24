import random
import logging
from urllib.request import Request
from fastapi import FastAPI
from starlette.responses import JSONResponse
from events_store import EventStore
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

events_store = EventStore()


app = FastAPI(title="Сервис рекомендаций")


class RangeError(Exception):
    pass


@app.exception_handler(RangeError)
async def range_error_exception_handler(request: Request, exc: RangeError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},)


def get_sims(user_id: int, max_events: int) -> list[int]:
    hist = events_store.get(user_id, max_events)
    log.info(f'History: {hist}')
    sims = [sim_store.get(h, max_events) for h in hist]
    # print('all sims', sims)
    n = 0
    rs = []
    for s in sims:
        if len(s):
            rs.append(s)
            n += 1
    sims = []
    max_sim = max(max_events // max(n, 1), 1)
    for s in rs:
        sims += random.sample(s, max_sim)
    return sims


@app.get(
    "/recommendations",
    summary="Получение", tags=["Рекомендации"],
    description="""
        Возвращает персональные рекомендации для пользователя, при их наличии, иначе рекомендации по умолчанию.
        Если имеется онлайн-история, то, к полученным выше описанным способом рекомендациям, подмешиваются похожие трэки
        """)
def recommendations(user_id: int, k: int = 10):
    if k > MAX_K or k <= 0:
        raise RangeError("k is out of range")
    sims = get_sims(user_id, k // 2 | 1)
    recs = rec_store.get(user_id, k)
    # print('Sims', sims)
    # print('Recs', recs)
    result = random.sample(set(sims + recs), k)
    # print(result)
    return {"recs": result}


@app.post(
    "/store_event",
    summary="Добавление", tags=["Событие"],
    description="""
        Сохраняет событие для пользователя в онлайн-истории
    """)
def store_event(user_id: int, item_id: int):
    events_store.put(user_id, item_id)
    return JSONResponse(
        status_code=201,
        content={"message": f"{item_id} stored for {user_id}"})


@app.get("/")
def root():
    return "recommendations service"
