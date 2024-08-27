import random
import logging
from urllib.request import Request
from fastapi import FastAPI
from starlette.responses import JSONResponse
from history_store import EventStore, Recommendations, SimilarItems


REC_COLUMNS = ["user_id", "item_id", "score", "tracks_total", "hearing_days", "tracks_per_day", "nusers", "rank"]
DEF_COLUMMS = ["track_id", "users", ]
SIM_COLUMNS = ["score", "track_id_1", "track_id_2"]

MAX_K = 100
log = logging.getLogger("uvicorn.error")

rec_store = Recommendations()
rec_store.load(
    "personal",
    'recommendations.parquet',
    columns=REC_COLUMNS,
)
rec_store.load(
    "default",
    'top_popular.parquet',
    columns=DEF_COLUMMS,
)

sim_store = SimilarItems()
sim_store.load(
    "similar.parquet",
    columns=SIM_COLUMNS
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
    all_similar_items = [sim_store.get(h, max_events) for h in hist]
    # print('all sims', sims)
    non_empty_count = 0
    non_empty_similars = []
    for similar_items_for_specific_track in all_similar_items:
        if len(similar_items_for_specific_track):
            non_empty_similars.append(similar_items_for_specific_track)
            non_empty_count += 1
    all_similar_items = []
    max_sim = max(max_events // max(non_empty_count, 1), 1)
    for similar_items_for_specific_track in non_empty_similars:
        all_similar_items += random.sample(similar_items_for_specific_track, max_sim)
    return all_similar_items


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
