from datetime import datetime

from forex_python.converter import CurrencyRates


def get_exchange_rate(curr_from, date_str=None):
    rates = CurrencyRates()
    date_of_rates = datetime.strptime(date_str, '%Y-%m-%d') if date_str else datetime.now()
    try:
        result = rates.get_rates(curr_from, date_of_rates)
    except Exception as e:
        result = None
    return result
