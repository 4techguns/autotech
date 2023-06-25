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

    if sc1from > sc1to:
        logging.error("CAT1 RANGE INVALID! FROM > TO")
    if sc2from > sc2to:
        logging.error("CAT2 RANGE INVALID! FROM > TO")
    if sc3from > sc3to:
        logging.error("CAT3 RANGE INVALID! FROM > TO")

    sortedc1 = store["cat1"][sc1from:sc1to]
    sortedc2 = store["cat2"][sc2from:sc2to]
    sortedc3 = store["cat3"][sc3from:sc3to]

    combined = sortedc1 + sortedc2 + sortedc3

    final = str.join(" ", list(dict.fromkeys(combined)))

    return generator.util.random_transform(final)