import re
from calendar import monthrange
import datetime


class CreditCard(object):
    """
    A credit card that may be valid or invalid.
    """
    # A regexp for matching non-digit values
    non_digit_regexp = re.compile(r'\D')

    def __init__(self, number, month, year, cvc, holder=None):
        self.number = self.non_digit_regexp.sub('', number)
        self.exp_date = ExpDate(month, year)
        self.cvc = cvc
        self.holder = holder


    @property
    def is_expired(self):
        return self.exp_date.is_expired

    @property
    def is_mod10_valid(self):
        """
        Luhn algorithm
        """
        # Check for empty string
        if not self.number:
            return False

        # Run mod10 on the number
        dub, tot = 0, 0
        for i in range(len(self.number) - 1, -1, -1):
            for c in str((dub + 1) * int(self.number[i])):
                tot += int(c)
            dub = (dub + 1) % 2

        return (tot % 10) == 0

    @property
    def is_valid(self):
        return not self.is_expired and self.is_mod10_valid
    
    @property
    def is_cvc_valid(self):
        if self.cvc:
            return True if len(self.cvc) == 3 else False
        else:
            return True


class ExpDate(object):
    """
    An expiration date of a credit card.
    """
    def __init__(self, month, year):
        """
        Attaches the last possible datetime for the given month and year, as
        well as the raw month and year values.
        """
        # Attach month and year
        self.month = month
        self.year = year

        # Get the month's day count
        weekday, day_count = monthrange(year, month)

        # Attach the last possible datetime for the provided month and year
        self.expired_after = datetime.datetime(
            year,
            month,
            day_count,
            23,
            59,
            59,
            999999
        )

    @property
    def is_expired(self):
        # Get the current datetime in UTC
        utcnow = datetime.datetime.utcnow()
        return utcnow > self.expired_after

    