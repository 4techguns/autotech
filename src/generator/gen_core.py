import random
import logging

import generator.util

def try_generate(store: dict):
    sc1from = int(abs(len(store["cat2"]) + len(store["cat3"])) / len(store["cat1"]))
    sc1to = int(abs(len(store["cat2"]) + len(store["cat3"])) / random.randint(min(2, len(store["cat1"])), len(store["cat1"])))
    sc2from = int(abs(len(store["cat1"]) - len(store["cat3"])) / len(store["cat2"]))
    sc2to = int(abs(len(store["cat1"]) - len(store["cat3"])) / random.randint(min(2, len(store["cat2"])), len(store["cat2"])))
    sc3from = int(abs(len(store["cat1"]) * len(store["cat2"])) / len(store["cat3"]))
    sc3to = int(abs(len(store["cat1"]) * len(store["cat2"])) / random.randint(min(2, len(store["cat3"])), len(store["cat3"])))

    logging.debug(f"ranges: 1[{sc1from}:{sc1to}] 2[{sc2from}:{sc2to}] 3[{sc3from}:{sc3to}]")
    logging.debug(f"store: 1:{len(store['cat1'])} 2:{len(store['cat2'])} 3:{len(store['cat3'])}")

    if sc1from > len(store["cat1"]): logging.warning("cat1 start range is greater than cat1's length")
    if sc2from > len(store["cat2"]): logging.warning("cat2 start range is greater than cat2's length")
    if sc3from > len(store["cat3"]): logging.warning("cat3 start range is greater than cat3's length")

    if sc1to > len(store["cat1"]): logging.warning("cat1 end range is greater than cat1's length")
    if sc2to > len(store["cat2"]): logging.warning("cat2 end range is greater than cat2's length")
    if sc3to > len(store["cat3"]): logging.warning("cat3 end range is greater than cat3's length")

    sortedc1 = store["cat1"][sc1from:sc1to]
    sortedc2 = store["cat2"][sc2from:sc2to]
    sortedc3 = store["cat3"][sc3from:sc3to]

    combined = sortedc1 + sortedc2 + sortedc3

    final = str.join(" ", combined)

    return generator.util.random_transform(final)