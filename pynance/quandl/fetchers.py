import Quandl


def economic_indicator(source, country, indicator, **kwargs):
    dataset = "{source}/{country}_{indicator}".format(
        source=source.upper(),
        country=country.upper(),
        indicator=indicator.upper()
    )
    return Quandl.get(dataset, **kwargs)
        

class Fundamentals(object):
    '''
    Wrapper for the stock fundamentals portion
    of the Quandl API. Initialize with a ticker symbol and
    call .get('some ratio code') with a code or list of codes.
    '''
    
    def __init__(self, symbol):
        self.symbol = symbol.upper()
    
    def dataset_code(self, ratios):
        code = 'DMDRN/' + self.symbol
        codes = []
        if type(ratios) == list:
            for r in ratios:
                codes.append(code + '_' + r.upper())
            return codes
        else:
            return code + '_' + ratios.upper()
    
    def get(self, ratios, **kwargs):
        dataset_code = self.dataset_code(ratios)
        return Quandl.get(dataset_code, **kwargs)
        
    def all_stats(self, **kwargs):
        return self.get('ALLFINANCIALRATIOS', **kwargs)

        