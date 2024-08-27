import random
import logging
from urllib.request import Request
from fastapi import FastAPI
from starlette.responses import JSONResponse
from history_store import EventStore, Recommendations, SimilarItems


rec_columns = ["user_id", "item_id", "score", "tracks_total", "hearing_days", "tracks_per_day", "nusers", "rank"]
def_columms = ["track_id", "users", ]
sim_columns = ["score", "track_id_1", "track_id_2"]

MAX_K = 100
log = logging.getLogger("uvicorn.error")

rec_store = Recommendations()
rec_store.load(
    "personal",
    'recommendations.parquet',
    columns=rec_columns,
)
rec_store.load(
    "default",
    'top_popular.parquet',
    columns=def_columms,
)

sim_store = SimilarItems()
sim_store.load(
    "similar.parquet",
    columns=sim_columns
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
    similars = [sim_store.get(h, max_events) for h in hist]
    # print('all sims', sims)
    non_empty_count = 0
    rs = []
    for si in similars:
        if len(si):
            rs.append(si)
            non_empty_count += 1
    similars = []
    max_sim = max(max_events // max(non_empty_count, 1), 1)
    for si in rs:
        similars += random.sample(si, max_sim)
    return similars


@app.get(
    "/recommendations",
    summary="Получение", tags=["Рекомендации"],
    description="""
        Возвращает персональные рекомендации для пользователя, при их наличии, иначе рекомендации по умолчанию.
        Если имеется онлайн-история, то, к полученным выше описанным способом рекомендациям, подмешиваются похожие трэки
        """)
def recommendations(user_id: int, k: int = 10):
    if k > MAX_K or k <= 0:
        raise RangeError("k is out of range, allowed values [1..100]")
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
