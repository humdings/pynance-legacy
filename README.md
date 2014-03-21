pynance
=======

Python financial data library for working with quandl and yahoo finance data.



```
from pynance import *


>>> # Save all financial ratio data from quandl.
>>> tickers = ['DD','AA','MMM']
>>> dm = DataManager(tickers)
>>> dm.save_companies()
>>> 
>>> # save a csv named by date with company:ratio as the rows:cols for each date
>>> dm.save_date_csv()
>>>
>>> # Save a csv named by the ratio with ticker:date as the rows:cols
>>> dm.save_field_csv()
>>>
>>>
>>> # Make a portfolio of historical data
>>> P = Portfolio(['MMM', 'DD', 'AA'], '2014-02-01','2014-03-01') # date time objects work too
>>> P.prices
               AA     DD     MMM
Date                            
2014-02-28  11.74  66.62  134.73
2014-02-27  12.03  66.00  134.34
2014-02-26  12.05  65.51  132.86
2014-02-25  11.62  64.92  132.93
2014-02-24  11.77  64.58  132.20
2014-02-21  11.73  64.87  131.57
2014-02-20  11.78  65.35  131.56
2014-02-19  11.76  64.26  130.56
2014-02-18  11.40  64.71  131.80
2014-02-14  11.37  64.50  132.12
2014-02-13  11.40  63.98  130.14
2014-02-12  11.27  63.51  130.44
2014-02-11  11.33  63.84  130.12
2014-02-10  11.06  63.01  128.85
2014-02-07  11.19  63.01  129.48
2014-02-06  11.05  62.52  128.06
2014-02-05  11.04  61.47  126.53
2014-02-04  11.42  61.18  125.89
2014-02-03  11.20  59.57  123.09

>>>
>>> P.volumes
                  AA        DD      MMM
Date                                   
2014-02-28  19015500   4689300  3179400
2014-02-27  15466500   5119900  3124000
2014-02-26  32810600   4002700  2771100
2014-02-25  21331000   3684800  2863100
2014-02-24  16780900   5521100  2454300
2014-02-21  20272300   4887100  2574300
2014-02-20  22289600   5277400  2155800
2014-02-19  33420700   3778000  2719400
2014-02-18  14298100   4897000  2876500
2014-02-14  11462800   3564300  3030000
2014-02-13  11953500   2964400  2850600
2014-02-12  16103000   3886100  2100600
2014-02-11  20566000   4536500  2604000
2014-02-10  22175600   4315900  3317400
2014-02-07  15312300   4627200  3263200
2014-02-06  22107800   4938300  3828400
2014-02-05  36519500   6049100  4960000
2014-02-04  19897100  15052700  7412500
2014-02-03  26572300   5928600  4245100

>>> # Current quotes from yahoo
>>> P.quotes
                                       AA       DD      MMM
avg_daily_volume              2.73167e+07  4479600  2905540
book_value                          9.839   17.252   26.386
change                                0.1      0.4     0.69
dividend_per_share                   0.12      1.8     2.76
dividend_yield                       1.01      2.7     2.08
earnings_per_share                  -2.14    5.182     6.72
ebitda                             2.556B   5.869B   8.037B
fifty_day_moving_avg              11.6891  64.8429  131.265
fifty_two_week_high                 12.38    67.95   140.43
fifty_two_week_low                   7.63    48.21   102.89
market_cap                        12.943B  62.138B  88.218B
one_yr_target_price                  9.97    67.43   141.12
pct_change_from_200_day_MA        +20.70%   +8.42%   +3.82%
pct_change_from_50_day_MA          +2.75%   +3.30%   +1.41%
price                               12.01    66.98   133.12
price_book_ratio                     1.21     3.86     5.02
price_earnings_growth_ratio          1.05     1.92     1.79
price_earnings_ratio                  N/A    12.85    19.71
price_sales_ratio                    0.56     1.72     2.84
revenue                           23.032B  35.935B  30.871B
short_ratio                           5.7        6      1.9
stock_exchange                       NYSE     NYSE     NYSE
two_hundred_day_moving_avg         9.9507  61.7791   128.22
volume                       3.242145e+07  6827455  5920375
```


