import logging
import pandas as pd


log = logging.getLogger("uvicorn.error")


class SimilarItems:

    def __init__(self):
        self._similar_items = None

    def load(self, path, **kwargs):
        log.info(f"Loading similar items ({path})")
        self._similar_items = pd.read_parquet(path, **kwargs)
        self._similar_items = self._similar_items.set_index("track_id_1")
        log.info(f"Similar items loaded")

    def get(self, item_id: int, k: int = 10):
        try:
            i2i = self._similar_items.loc[item_id].head(k)
            print(i2i)
            i2i = i2i[["item_id_2", "score"]].to_dict()
        except KeyError:
            log.error(f"No similar items found for {item_id}")
            i2i = {"item_id_2": [], "score": {}}

        return i2i

