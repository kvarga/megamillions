megamillions
============
This is a bare-bones script for trying to figure out how much you get from MegaMillions tickets. 

Setup Instructions
==================
    pip install -r requirements.txt
    python -c 'import lotto;lotto.define_tables()'


Import Instructions
===============
1. Update test.csv with your lottery numbers
2. Run

```
python -c 'import lotto;lotto.import_from_csv("{yourusername}", "test.csv")'
```

Run Instructions
=============
    python -c 'import lotto;lotto.find_winners()'
