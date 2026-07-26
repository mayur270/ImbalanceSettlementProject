"""Below is a PriceTracker that uses a segment tree to retrieve/ update data.

--- Assumptions ---
1. Price updates are sequential
2. Does not handle BST (British Summer Time) periods
3. No initial prices e.g. self._prices = [None] * 48, otherwise segment tree
would need to be built beforehand which would be O(n) time complexity.

--- Segment Tree Time Complexity ---
update_price(period, price)          O(log n)
get_price(period)                    O(1)
get_price_range(start, end)          O(n)
get_highest_price()                  O(1)
get_lowest_price()                   O(1)

Segment Tree Space Complexity: O(n)

--- Memory usage approx. ---
Price Array: (48 * 24 bytes) + (56 bytes (empty list) + list pointers (48 * 8)) = 1592 bytes or 1.6KB + overallocation
Min Tree: ((95 * 24 bytes) + 16) + (56 bytes (empty list) + list pointers (128 * 8)) + overallocation = 3376 bytes or 3.3KB
Max Tree: ((95 * 24 bytes) + 16) + (56 bytes (empty list) + list pointers (128 * 8)) + overallocation = 3376 bytes or 3.3KB

Total = 8.2KB
"""

from time import monotonic
from typing import Optional

_TREE_SIZE = 64 # 2^6
_TREE_LEN = _TREE_SIZE * 2 # 128


class PriceTracker:

    def __init__(self):
        # Set fixed size (similar approach to 'seen' in validate.py file)
        self._prices = [None] * 48

        self._max_tree = [None] * _TREE_LEN
        self._min_tree = [None] * _TREE_LEN

    def get_price(self, period: int):
        """Get price. Slicing or Indexing uses 0(1) operation

        :param period: HH period
        """
        self.validate_period_data(period)
        return self._prices[period - 1]

    def get_price_range(self, start_period: int, end_period: int) -> list:
        """Gets prices from period range. This function will not return None values.
        :param start_period: Pick any start period starting from 1 (inclusive)
        :param end_period: Pick any end period until 48 (inclusive)
        :return: [(period, price),] or ValueError
        """
        self.validate_period_data(start_period)
        self.validate_period_data(end_period)

        if start_period > end_period:
            raise ValueError(
                "Start period cannot be greater than end period."
            )

        result = []

        for period in range(start_period, end_period + 1):
            price = self._prices[period - 1]

            if price is not None:
                result.append((period, price))

        return result

    def update_price(self, period: int, price: float) -> None:
        """
        :param period: Refers to HH settlement period from 0 to 47 for the day.
        :param price: Price for a specific period.
        :return: None
        """
        self.validate_period_data(period)

        if price <= 0.0: # Float positive does not include 0
            raise ValueError("price must be positive, got %r" % price)

        # -1 due to Python starting from 0
        index = period - 1
        self._prices[index] = price
        self._update_path_to_root(index)

    def get_maximum_price(self) -> Optional[tuple]:
        """Get the maximum value from 48 settlement period."""
        max_index = self._max_tree[1]
        if max_index is None:
            return None
        period = max_index + 1
        return period, self._prices[max_index]

    def get_minimum_price(self) -> Optional[tuple]:
        """Get the minimum value from 48 settlement period."""
        min_index = self._min_tree[1]
        if min_index is None:
            return None
        period = min_index + 1
        return period, self._prices[min_index]

    def _update_path_to_root(self, index: int):
        r"""This function creates parents from child nodes. e.g. it starts at the leaf
        nodes and works upwards. For max tree if the prices were [1, 2, 3, 4], then
        global max would be 4. 4 should be at the root as shown below.

              4
             / \
           2    4
          / \  / \
         1  2 3   4

        :param index: index value
        """

        # Checking if price is None or not None
        if self._prices[index] is not None:
            leaf = index
        else:
            leaf = None

        # Tree size in the array implementation
        tree_index = _TREE_SIZE + index
        self._min_tree[tree_index] = leaf
        self._max_tree[tree_index] = leaf

        # Get min/ max per level of tree height from leaf to root
        while tree_index > 1:

            tree_index //= 2 # floor divisor for parent
            left = 2 * tree_index
            right = left + 1

            # Update min tree
            self._min_tree[tree_index] = self._compare_price_indices(
                self._min_tree[left], self._min_tree[right], True)

            # Update max tree
            self._max_tree[tree_index] = self._compare_price_indices(
                self._max_tree[left], self._max_tree[right], False)


    def _compare_price_indices(
            self, left_index: int, right_index: int, want_min: bool
    ):
        """ Makes comparison between left and right index.
        If both are same choose lower index.
        """
        # Return right index if left index is None and vice versa
        if left_index is None:
            return right_index

        if right_index is None:
            return left_index

        # Get prices to check which is lower/ higher
        left_price = self._prices[left_index]
        right_price = self._prices[right_index]

        if left_price < right_price:
            return left_index if want_min else right_index

        if right_price < left_price:
            return right_index if want_min else left_index

        # Checking ties - takes lower index
        index = left_index if left_index < right_index else right_index
        return index

    def validate_period_data(self, period):
        if period < 1 or period > 48:
            raise ValueError(
                "Period range should be from 1 to 48."
            )


if __name__ == "__main__":

    tracker = PriceTracker()

    print("\n--- Prices after initial updates ---")
    tracker.update_price(1, 50.0)
    tracker.update_price(2, 30.0)
    tracker.update_price(3, 70.0)
    tracker.update_price(4, 40.0)
    tracker.update_price(5, 30.0)
    tracker.update_price(8, 90.0)

    # Checking prices
    print(tracker._prices)

    print("\n--- Get Price lookup ---")

    start_get_price = monotonic()
    print("Period 3:", tracker.get_price(3))
    end_get_price = monotonic() - start_get_price
    start_get_max = monotonic()
    print("Highest:", tracker.get_maximum_price())
    end_get_max = monotonic() - start_get_max
    start_get_min = monotonic()
    print("Lowest:", tracker.get_minimum_price())
    end_get_min = monotonic() - start_get_min

    print("\n--- Get Price Range ---")
    start_get_price_range = monotonic()
    print(tracker.get_price_range(1, 48))
    end_get_price_range = monotonic() - start_get_price_range

    print("\n--- Update Existing Price ---")
    start_update_price = monotonic()
    tracker.update_price(8, 200.0)
    end_update_price = monotonic() - start_update_price

    print("Prices after update:")
    print(tracker._prices)
    print("Highest:", tracker.get_maximum_price())
    print("Lowest:", tracker.get_minimum_price())

    print("\n--- Update price - Checking for tie ---")
    tracker.update_price(11, 200.0)

    print("Prices after update:")
    print(tracker._prices)
    print("Highest:", tracker.get_maximum_price())
    print("Lowest:", tracker.get_minimum_price())

    print("\n--- Time ---")
    print(f"Get Price Time: {end_get_price * 1000:.5f} ms")
    print(f"Get Price Range Time: {end_get_price_range * 1000:.5f} ms")
    print(f"Get Update Price Time: {end_update_price * 1000:.5f} ms")
    print(f"Get Max Time: {end_get_max * 1000:.5f} ms")
    print(f"Get Min Time: {end_get_min * 1000:.5f} ms")
