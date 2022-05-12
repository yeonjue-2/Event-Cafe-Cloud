from enum import Enum


class Category(str, Enum):
    KPOP = "K-POP"
    ANIMATION = "Animation"
    INFLUENCER = "Influencer"
    WEBTOON = "Webtoon"
    NOVEL = "Novel"

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
