import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from recommendations import Recommendations
import requests


features_store_url = "http://127.0.0.1:8010"
events_store_url = "http://127.0.0.1:8020"

logger = logging.getLogger("uvicorn.error")

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(app.title)
    logger.info("Starting")

    yield
    logger.info("Stopping")


app = FastAPI(title="recommendations", lifespan=lifespan)


@app.post("/recommendations")
async def recommendations(user_id: int, k: int = 10):
    recs = rec_store.get(user_id, k)
    return {"recs": recs}


def dedup_ids(ids):
    seen = set()
    ids = [id for id in ids if not (id in seen or seen.add(id))]

    return ids


# @app.post("/recommendations_online")
# async def recommendations_online(user_id: int, k: int = 100):
#     """
#     Возвращает список онлайн-рекомендаций длиной k для пользователя user_id
#     """
#
#     headers = {"Content-type": "application/json", "Accept": "text/plain"}
#
#     # получаем последнее событие пользователя
#     params = {"user_id": user_id, "k": 1}
#     resp = requests.post(events_store_url + "/get", headers=headers, params=params)
#     events = resp.json()
#     events = events["events"]
#     print(events)
#
#     # получаем список похожих объектов
#     if len(events) > 0:
#         item_id = events[0]
#         params = {"item_id": item_id, "k": k}
#         item_similar_items = requests.post(features_store_url + "/similar_items", headers=headers, params=params)
#         item_similar_items = item_similar_items.json()
#         print(item_similar_items)
#         recs = item_similar_items  #item_similar_items[:k]
#     else:
#         recs = []
#
#     return {"recs": recs}

@app.get("/")
def root():
    return "recommendations service"
