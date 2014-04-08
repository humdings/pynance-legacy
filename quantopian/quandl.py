
import datetime

import pandas as pd


class QuandlFetcher(object):
    
    API_URL = 'http://www.quandl.com/api/v1/'
    
    def __init__(self, auth_token=None):
        self.auth_token = auth_token
        
    def _append_query_fields(self, url, **kwargs):
        field_values = ['{0}={1}'.format(key, val)
                        for key, val in kwargs.items() if val]
        return url + 'request_source=python&request_version=2&' +'&'.join(field_values)
        
    def _parse_dates(self, date):
        if date is None:
            return date
        if isinstance(date, datetime.datetime):
            return date.date().isoformat()
        if isinstance(date, datetime.date):
            return date.isoformat()
        try:
            date = pd.to_datetime(date)
        except ValueError:
            raise ValueError("{} is not recognised a date.".format(date))
        return date.date().isoformat()

    def build_url(self, dataset, **kwargs):
        """Return dataframe of requested dataset from Quandl.
    
        :param dataset: str or list, depending on single dataset usage or multiset usage
                Dataset codes are available on the Quandl website
        :param str trim_start, trim_end: Optional datefilers, otherwise entire
            dataset is returned
        :param str collapse: Options are daily, weekly, monthly, quarterly, annual
        :param str transformation: options are diff, rdiff, cumul, and normalize
        :param int rows: Number of rows which will be returned
        :param str sort_order: options are asc, desc. Default: `asc`
        :param str text: specify whether to print output text to stdout, pass 'no' to supress output.
        :returns: :class:`pandas.DataFrame` or :class:`numpy.ndarray`
    
        Note that Pandas expects timeseries data to be sorted ascending for most
        timeseries functionality to work.
    
        Any other `kwargs` passed to `get` are sent as field/value params to Quandl
        with no interference.
    
        """
        auth_token = self.auth_token
        kwargs.setdefault('sort_order', 'asc')
        trim_start = self._parse_dates(kwargs.pop('trim_start', None))
        trim_end = self._parse_dates(kwargs.pop('trim_end', None))
    
        #Check whether dataset is given as a string (for a single dataset) or an array (for a multiset call)
        
        
        #Unicode String
        if type(dataset) == unicode or type(dataset) == str:
            url = self.API_URL + 'datasets/{}.csv?'.format(dataset)
        
        #Array
        elif type(dataset) == list:
            url = self.API_URL + 'multisets.csv?columns='
            #Format for multisets call
            dataset = [d.replace('/', '.') for d in dataset]
            for i in dataset:
                url += i + ','
            #remove trailing ,
            url = url[:-1] + '&'
            
        #If wrong format
        else:
            error = "Your dataset must either be specified as a string (containing a Quandl code) or an array (of Quandl codes) for multisets"
            raise Exception(error)
            
        url = self._append_query_fields(
            url,
            auth_token=auth_token,
            trim_start=trim_start,
            trim_end=trim_end,
            **kwargs
        )
        return url

def _download(url):
    '''
    Used to download data outside of Quantopian.
    '''
    dframe = pd.read_csv(url, index_col=0, parse_dates=True)
    return dframe
