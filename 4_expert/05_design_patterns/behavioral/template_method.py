"""
Template Method Design Pattern

The Template Method pattern defines the skeleton of an algorithm in a method,
deferring some steps to subclasses. It lets subclasses redefine certain steps
of an algorithm without changing the algorithm's structure.

Key components:
1. AbstractClass: Defines abstract primitive operations that concrete subclasses must implement
                 Implements a template method which defines the skeleton of an algorithm
2. ConcreteClass: Implements the primitive operations to carry out subclass-specific steps

This pattern is commonly used in frameworks where they provide the overall structure
of an algorithm but let the specific steps be defined by user implementations.
"""

from abc import ABC, abstractmethod
import time


# Abstract Class
class DataProcessor(ABC):
    """
    The Template Method pattern: defines the skeleton of the data processing
    algorithm, with concrete steps implemented by subclasses.
    """
    
    def template_method(self, data):
        """
        The template method defines the skeleton of the algorithm.
        """
        start_time = time.time()
        
        # Steps of the algorithm
        processed_data = self.read_data(data)
        processed_data = self.parse_data(processed_data)
        processed_data = self.transform_data(processed_data)
        result = self.analyze_data(processed_data)
        self.send_data(result)
        
        # Common post-processing
        end_time = time.time()
        self.log_performance(end_time - start_time)
        
        return result
    
    # These methods are "hooks" that can be overridden by subclasses
    def log_performance(self, execution_time):
        """Hook method that can be overridden"""
        print(f"Data processing completed in {execution_time:.4f} seconds")
    
    # These are abstract methods that must be implemented by subclasses
    @abstractmethod
    def read_data(self, data):
        pass
    
    @abstractmethod
    def parse_data(self, data):
        pass
    
    @abstractmethod
    def transform_data(self, data):
        pass
    
    @abstractmethod
    def analyze_data(self, data):
        pass
    
    @abstractmethod
    def send_data(self, data):
        pass


# Concrete implementations
class TextDataProcessor(DataProcessor):
    """Processes text data."""
    
    def read_data(self, data):
        print("Reading text data...")
        return data
    
    def parse_data(self, data):
        print("Parsing text...")
        # Simulated parsing of text data
        return [word.lower() for word in data.split()]
    
    def transform_data(self, data):
        print("Transforming text data...")
        # Simulated transformation (removing short words)
        return [word for word in data if len(word) > 3]
    
    def analyze_data(self, data):
        print("Analyzing text data...")
        word_counts = {}
        for word in data:
            word_counts[word] = word_counts.get(word, 0) + 1
        return word_counts
    
    def send_data(self, data):
        print("Sending text analysis results...")
        print(f"Word frequency analysis: {data}")


class NumericDataProcessor(DataProcessor):
    """Processes numeric data."""
    
    def read_data(self, data):
        print("Reading numeric data...")
        return data
    
    def parse_data(self, data):
        print("Parsing numeric data...")
        # Convert string numbers to float
        return [float(x) for x in data.split()]
    
    def transform_data(self, data):
        print("Transforming numeric data...")
        # Normalization by dividing by the maximum value
        max_value = max(data) if data else 1
        return [x / max_value for x in data]
    
    def analyze_data(self, data):
        print("Analyzing numeric data...")
        if not data:
            return {"count": 0, "sum": 0, "avg": 0, "min": 0, "max": 0}
        
        return {
            "count": len(data),
            "sum": sum(data),
            "avg": sum(data) / len(data),
            "min": min(data),
            "max": max(data)
        }
    
    def send_data(self, data):
        print("Sending numeric analysis results...")
        print(f"Statistics: {data}")
    
    # Override hook method
    def log_performance(self, execution_time):
        print(f"Numeric data processing completed in {execution_time:.4f} seconds")
        print(f"Average processing time per data point: {execution_time / (data['count'] if data['count'] > 0 else 1):.6f} seconds")


# Custom processor with additional steps
class EnhancedTextProcessor(TextDataProcessor):
    """Enhanced text processor with additional functionality."""
    
    def transform_data(self, data):
        print("Performing enhanced text transformation...")
        # First apply the base transformation
        transformed_data = super().transform_data(data)
        # Then enhance with stemming (simplified simulation)
        result = []
        for word in transformed_data:
            # Simplified stemming (removing common endings)
            if word.endswith('ing'):
                word = word[:-3]
            elif word.endswith('s'):
                word = word[:-1]
            result.append(word)
        return result
    
    # Add a new hook method
    def log_performance(self, execution_time):
        super().log_performance(execution_time)
        print(f"Enhanced processing enabled with stemming")


# Example usage
if __name__ == "__main__":
    # Process text data
    print("\n=== Processing Text Data ===")
    text_processor = TextDataProcessor()
    text_data = "The quick brown fox jumps over the lazy dog"
    text_result = text_processor.template_method(text_data)
    
    # Process numeric data
    print("\n=== Processing Numeric Data ===")
    numeric_processor = NumericDataProcessor()
    numeric_data = "14 25 37 8 92 65 41 33"
    numeric_result = numeric_processor.template_method(numeric_data)
    
    # Process text with enhanced processor
    print("\n=== Processing Text with Enhanced Processor ===")
    enhanced_processor = EnhancedTextProcessor()
    enhanced_result = enhanced_processor.template_method(text_data)