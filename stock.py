from requests_html import HTMLSession
import functools
from datetime import datetime
import utils


def try_property(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(str(e))
            return None
    return property(wrapper)


class Stock:
    def __init__(self, ticker: str):
        self.ticker_symbol = ticker.upper()
        self.refresh_values()

    def refresh_values(self):
        "refreshes stock statistics to present values"
        try:
            self.html_resp = HTMLSession().get(f'https://finance.yahoo.com/quote/{self.ticker_symbol}?p={self.ticker_symbol}')
        except Exception as e:
            print("Encountered exception: ", end="")
            print(e)
            print("Please verify network connectivity and the symbol you input")

        if hasattr(self, '_price'):
            del self._price

        if hasattr(self, '_daily_change_dollar'):
            del self._daily_change_dollar

        if hasattr(self, '_daily_change_percent'):
            del self._daily_change_percent

        if hasattr(self, '_previous_close'):
            del self._previous_close

        if hasattr(self, '_days_range'):
            del self._days_range

        if hasattr(self, '_open_price'):
            del self._days_range

        if hasattr(self, '_years_range'):
            del self._years_range

        if hasattr(self, '_volume'):
            del self._volume

        if hasattr(self, "_avg_volume"):
            del self._avg_volume

    @try_property
    def price(self):
        "gets the price of the stock"
        if not hasattr(self, '_price'):
            self._price = float(self.html_resp.html.find('.Trsdu\(0\.3s\).Fw\(b\).Fz\(36px\).Mb\(-4px\).D\(ib\)')[0].text)
        return self._price


    @try_property
    def daily_change_dollar(self):
        'gets the daily change in the stock in dollars'
        if not hasattr(self, '_daily_change_dollar'):
            self.get_daily_change()
        return self._daily_change_dollar

    @try_property
    def daily_change_percent(self):
        'gets the daily change in the stock in percent of its value'
        if not hasattr(self, '_daily_change_percent'):
            self._get_daily_change()
        return self._daily_change_percent

    def _get_daily_change(self):
        daily_change_string = self.html_resp.html.find('.Trsdu\(0\.3s\).Fw\(500\).Pstart\(10px\).Fz\(24px\).C\(\$dataRed\)')[0].text
        self._daily_change_dollar = float(daily_change_string.split(" ")[0])
        self._daily_change_percent = float(utils.kill_parens(daily_change_string.split(" ")[1]).replace("%", ""))


    @try_property
    def previous_close(self):
        'gets the previous close of the stock'
        if not hasattr(self, '_previous_close'):
            self._previous_close = float(next(filter(
                lambda x: x.attrs.get('data-reactid') == '43',
                self.html_resp.html.find('.Trsdu\(0\.3s\)'))).text)
        return self._previous_close

    @try_property
    def open_price(self):
        if not hasattr(self, '_open'):
            self._open = float(next(filter(
                lambda x: x.attrs.get('data-reactid') == '48',
                self.html_resp.html.find('.Trsdu\(0\.3s\)'))).text)
        return self._open

    @try_property
    def days_range(self):
        'a tuple of high and low for the stock today'
        if not hasattr(self, '_days_range'):
            self._days_range = tuple(map(float,
                                         self.html_resp.html.find('[data\-test=DAYS\_RANGE\-value]')[0].text.split(" - ")))
        return self._days_range


    @try_property
    def years_range(self):
        'a tuple of high and low for the stock in the last 52 weeks'
        if not hasattr(self, '_years_range'):
            self._years_range = tuple(map(float,
                                          self.html_resp.html.find('[data\-\test=FIFTY\_TWO\_WK\_RANGE\-value]')[0].text.split(" - ")))
        return self._years_range

    @try_property
    def volume(self):
        'volume for the stock'
        if not hasattr(self, '_volume'):
            self._volume = int(next(
                filter(lambda x: x.attrs.get('data-reactid') == '71',
                       self.html_resp.html.find(
                           '.Trsdu\(0\.3s\)'))).text.replace(",", ""))
        return self._volume

    @try_property
    def avg_volume(self):
        'avg volume for the stock'
        if not hasattr(self, '_avg_volume'):
            self._avg_volume = int(next(filter(
                lambda x: x.attrs.get('data-reactid') == '76',
                self.html_resp.html.find(
                    '.Trsdu\(0\.3s\)'))).text.replace(",", ""))
        return self._avg_volume

if __name__ == "__main__":
    print(Stock('BAC').avg_volume)
