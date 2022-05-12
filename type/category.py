from enum import Enum


class Category(str, Enum):
    KPOP = "kpop"
    ANIMATION = "animation"
    INFLUENCER = "influencer"
    WEBTOON = "webtoon"
    NOVEL = "novel"

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value
