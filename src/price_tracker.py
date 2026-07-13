class PriceTracker:

    # TODO: Needs to be completed.

    def __init__(self):
        # Set fixed size (similar approach to 'seen' in validate.py file)
        self._prices = [None] * 48

    def get_price(self, period):
        """Get price. Slicing or Indexing uses 0(1) operation

        :param period: HH period
        """
        return self._prices[period - 1]

    def get_price_range(self, start_period, end_period):
        """Gets prices from a range """
        if start_period > end_period:
            raise ValueError(
                "Start period cannot be greater than end period."
            )

        result = []
        for index in range(start_period - 1, end_period):
            if self._prices[index] is not None:
                result.append(self._prices[index])
        return result


# Testing and checking below
price_tracker = PriceTracker()
price_list = [
    None, 1, 4, 3, 6,
    7, None, None, 8, 9,
    None, 1, 4, 3, 6,
    11, None, None, 14, 9,
    None, 1, 12, 3, 14,
    7, None, None, None, 9,
    None, 1, None, 3, 6,
    7, None, None, 8, 9,
    None, 1, 4, 16, 15,
    7, None, None
]
price_tracker._prices = price_list
print(price_tracker.get_price(period=4)) # should expect 3

print(price_tracker.get_price_range(start_period=2, end_period=5)) # Should get [1, 4, 3, 6]
