## Generate output
Run time_align.py program

## Output folder
1. market_data_183.csv: contains 183 stocks that have both s&p rating and ratios / dividend records.
2. no_price_list.txt: 
contains gvkey of the stocks that no long has a price record at the end (probably no longer traded in the market), it is suggested to discard these stocks. 
Also, bear in mind that some stocks does no has a price intially, but has a price at a later point, we can discard those records with a 0 price.