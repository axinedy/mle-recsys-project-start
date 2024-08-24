import logging
import pandas as pd


log = logging.getLogger("uvicorn.error")


class Recommendations:

    def __init__(self):
        self._recs = {"personal": None, "default": None}
        self._stats = {
            "request_personal_count": 0,
            "request_default_count": 0,
        }

    def load(self, type, path, **kwargs):
        log.info(f"Loading recommendations, type: {type} ({path})")
        self._recs[type] = pd.read_parquet(path, **kwargs)
        if type == "personal":
            self._recs[type] = self._recs[type].set_index("user_id")
        log.info(f"Loaded: {type}")

    def get(self, user_id: int, k: int = 10):
        log.info(f"Recommendations.get {user_id}, {k}")
        try:
            recs = self._recs["personal"].loc[user_id]
            log.info(f'Found personal recommendations for user {user_id}')
            recs = recs.sample(k)["item_id"].to_list()
            print(recs)
            self._stats["request_personal_count"] += 1
        except KeyError:
            recs = self._recs["default"]
            log.info(f'Recommendations for user {user_id} not found, returning default')
            recs = recs.sample(k)["track_id"].to_list()
            self._stats["request_default_count"] += 1
        except Exception as e:
            print(f'{type(e)}: {e}')
            log.error("No recommendations found")
            recs = []
        return recs

    def stats(self):
        log.info("Stats for recommendations")
        for name, value in self._stats.items():
            log.info(f"{name:} {value} ")
