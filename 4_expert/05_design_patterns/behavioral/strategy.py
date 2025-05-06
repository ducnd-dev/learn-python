"""
Strategy Design Pattern

The Strategy pattern defines a family of algorithms, encapsulates each one, and makes them 
interchangeable. It lets the algorithm vary independently from clients that use it.

Key components:
1. Strategy: Common interface for all concrete strategies
2. ConcreteStrategy: Implements the algorithm using the Strategy interface
3. Context: Maintains a reference to a Strategy object and delegates algorithm execution to it

This pattern is useful when you want to define a class that will have one behavior that is similar
to other behaviors in a list, but is completely independent of clients.
"""

from abc import ABC, abstractmethod
from typing import List


# Strategy interface
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: List) -> List:
        pass


# Concrete Strategies
class BubbleSortStrategy(SortStrategy):
    def sort(self, data: List) -> List:
        print("Sorting using bubble sort")
        # Create a copy of the list to avoid modifying the original
        result = data.copy()
        n = len(result)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                if result[j] > result[j + 1]:
                    result[j], result[j + 1] = result[j + 1], result[j]
                    
        return result


class QuickSortStrategy(SortStrategy):
    def sort(self, data: List) -> List:
        print("Sorting using quick sort")
        # Create a copy of the list to avoid modifying the original
        result = data.copy()
        self._quick_sort(result, 0, len(result) - 1)
        return result
    
    def _quick_sort(self, data: List, low: int, high: int) -> None:
        if low < high:
            pivot_index = self._partition(data, low, high)
            self._quick_sort(data, low, pivot_index - 1)
            self._quick_sort(data, pivot_index + 1, high)
    
    def _partition(self, data: List, low: int, high: int) -> int:
        pivot = data[high]
        i = low - 1
        
        for j in range(low, high):
            if data[j] <= pivot:
                i += 1
                data[i], data[j] = data[j], data[i]
                
        data[i + 1], data[high] = data[high], data[i + 1]
        return i + 1


class MergeSortStrategy(SortStrategy):
    def sort(self, data: List) -> List:
        print("Sorting using merge sort")
        # Create a copy of the list to avoid modifying the original
        result = data.copy()
        
        if len(result) > 1:
            self._merge_sort(result)
            
        return result
    
    def _merge_sort(self, data: List) -> None:
        if len(data) > 1:
            mid = len(data) // 2
            left_half = data[:mid]
            right_half = data[mid:]
            
            self._merge_sort(left_half)
            self._merge_sort(right_half)
            
            i = j = k = 0
            
            while i < len(left_half) and j < len(right_half):
                if left_half[i] < right_half[j]:
                    data[k] = left_half[i]
                    i += 1
                else:
                    data[k] = right_half[j]
                    j += 1
                k += 1
                
            while i < len(left_half):
                data[k] = left_half[i]
                i += 1
                k += 1
                
            while j < len(right_half):
                data[k] = right_half[j]
                j += 1
                k += 1


# Context
class Sorter:
    def __init__(self, strategy: SortStrategy = None):
        self._strategy = strategy
    
    def set_strategy(self, strategy: SortStrategy) -> None:
        self._strategy = strategy
    
    def sort(self, data: List) -> List:
        if self._strategy is None:
            raise ValueError("Sorting strategy not set")
        return self._strategy.sort(data)


# Example usage
if __name__ == "__main__":
    # Sample data
    numbers = [5, 2, 8, 12, 3, 7, 9, 1]
    
    # Create context
    sorter = Sorter()
    
    # Use bubble sort strategy
    sorter.set_strategy(BubbleSortStrategy())
    sorted_numbers = sorter.sort(numbers)
    print(f"Bubble sort result: {sorted_numbers}")
    
    # Use quick sort strategy
    sorter.set_strategy(QuickSortStrategy())
    sorted_numbers = sorter.sort(numbers)
    print(f"Quick sort result: {sorted_numbers}")
    
    # Use merge sort strategy
    sorter.set_strategy(MergeSortStrategy())
    sorted_numbers = sorter.sort(numbers)
    print(f"Merge sort result: {sorted_numbers}")
    
    # Verify original list remained unchanged
    print(f"Original list: {numbers}")