"""
Observer Design Pattern

The Observer pattern defines a one-to-many dependency between objects so that
when one object changes state, all its dependents are notified and updated automatically.

Key components:
1. Subject (Observable): Maintains a list of observers and notifies them of state changes
2. Observer: Defines an updating interface for objects that should be notified of changes
3. ConcreteSubject: Stores state of interest to ConcreteObserver objects and sends notifications
4. ConcreteObserver: Maintains a reference to the ConcreteSubject and implements the Observer updating interface

Used for implementing distributed event handling systems and MVC architectures.
"""

from abc import ABC, abstractmethod
from typing import List


# Observer interface
class Observer(ABC):
    @abstractmethod
    def update(self, message: str) -> None:
        pass


# Subject (Observable)
class Subject:
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        try:
            self._observers.remove(observer)
        except ValueError:
            pass
    
    def notify(self, message: str) -> None:
        for observer in self._observers:
            observer.update(message)


# Concrete Subject
class NewsPublisher(Subject):
    def __init__(self):
        super().__init__()
        self._latest_news = ""
    
    def add_news(self, news: str) -> None:
        self._latest_news = news
        self.notify(self._latest_news)


# Concrete Observers
class EmailSubscriber(Observer):
    def __init__(self, name: str):
        self.name = name
    
    def update(self, message: str) -> None:
        print(f"Email to {self.name}: {message}")


class SMSSubscriber(Observer):
    def __init__(self, name: str):
        self.name = name
    
    def update(self, message: str) -> None:
        print(f"SMS to {self.name}: {message}")


class AppNotificationSubscriber(Observer):
    def __init__(self, name: str):
        self.name = name
    
    def update(self, message: str) -> None:
        print(f"App notification to {self.name}: {message}")


# Example usage
if __name__ == "__main__":
    news_publisher = NewsPublisher()
    
    # Create subscribers
    john_email = EmailSubscriber("John")
    sara_sms = SMSSubscriber("Sara")
    mike_app = AppNotificationSubscriber("Mike")
    sara_app = AppNotificationSubscriber("Sara")
    
    # Register subscribers
    news_publisher.attach(john_email)
    news_publisher.attach(sara_sms)
    news_publisher.attach(mike_app)
    news_publisher.attach(sara_app)
    
    # Publish news
    print("\n> Breaking news published:")
    news_publisher.add_news("Breaking News: Python 4.0 Released!")
    
    # Sara unsubscribes from SMS notifications
    news_publisher.detach(sara_sms)
    
    # Publish another news
    print("\n> Technology update published:")
    news_publisher.add_news("Technology Update: New AI Framework Announced")