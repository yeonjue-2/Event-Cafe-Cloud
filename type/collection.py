from enum import Enum


class Collection(str, Enum):
    EVENTS = 'events'
    CAFES = 'cafes'
    REVIEWS = 'reviews'
    HEARTS = 'hearts'
    POSTS = 'posts'

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
