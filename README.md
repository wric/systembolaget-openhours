# Systembolaget Openhours

This package helps the user fetch info from Systembolagets open API. When the
stores are feched it's possible to get and evaluate open hours 16 days ahead
for all the stores.

## Examples

### Evaluate if store has deviating open hours

```py
from systembolaget_openhours.fetcher import Fetcher

fetcher = Fetcher()
store = fetcher.get_store_by_name("Backaplan")
store.has_deviation()  # True / False
```

### Evaluate specific date for store

**Note:** you can only evaluate today date and 15 days ahead.

```py
from systembolaget_openhours.fetcher import Fetcher

fetcher = Fetcher()
store = fetcher.get_store_by_no("1414")
store.is_datestring_deviating("2020-05-21")  # True / False
```

### Print deviations

```py
from systembolaget_openhours.fetcher import Fetcher

fetcher = Fetcher()
store = fetcher.get_store_by_no("1414")

for is_deviation, info in store.get_all_evaluations():
    if is_deviation:
        print(f"Deviation due to: {info}")
        # "Deviation due to: Julafton"
```

## Miscellaneous

This is a weekend hack that probably contains multiple bugs :) Open an issue if
you find any bug and I'll take a look at it when I got time.
