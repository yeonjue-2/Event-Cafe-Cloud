from enum import Enum


class Collection(str, Enum):
    USERS = 'users'
    USERS_PK = 'user_id'

    EVENTS = 'events'
    EVENTS_PK = 'event_id'

    CAFES = 'cafes'
    CAFES_PK = 'cafe_id'

    REVIEWS = 'reviews'
    REVIEWS_PK = 'review_id'

    HEARTS = 'hearts'
    HEARTS_PK = 'heart_id'

    POSTS = 'posts'
    POSTS_PK = 'post_id'

    BOOKMARKS = 'bookmarks'
    BOOKMARKS_PK = 'bookmark_id'

    CUSTOMS = 'customs'
    CUSTOMS_PK = 'custom_id'

    PAYMENTS = 'payments'
    PAYMENTS_PK = 'payment_id'

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value
