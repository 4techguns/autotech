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

def try_generate_dbg(store: dict):
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

    return f"""
```ansi
[2;41m[0m[2;40m[0m[2;45m  [0m = cat 1
[2;40m  [0m[2;45m[0m = cat 2
[2;44m  [0m = cat 3

ranges      : [2;45m[2;37m {sc1from}:{sc1to} [2;40m {sc2from}:{sc2to} [2;43m {sc3from}:{sc3to} [0m[2;37m[2;40m[0m[2;37m[2;45m[0m[2;45m
[0mstored words: [2;45m[2;37m {len(store['cat1'])} [2;40m {len(store['cat2'])} [2;43m {len(store['cat3'])} [0m[2;37m[2;40m[0m[2;37m[2;45m[0m[2;45m[0m

[2;45m[0m[2;37m[0m[2;45m[2;37m{str.join(" ", sortedc1)}[0m[2;45m[0m [2;40m[2;37m{str.join(" ", sortedc2)}[0m[2;40m[0m [2;44m[2;37m{str.join(" ", sortedc3)}[0m[2;44m[0m[2;42m[0m
```
    """