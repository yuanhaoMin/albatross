from enum import Enum


class SubscriptionPlanEnum(Enum):
    BASIC_01 = (1, 43, 1)
    BASIC_02 = (2, 86, 1)
    BASIC_03 = (3, 122, 1)
    BASIC_04 = (4, 163, 1)
    BASIC_05 = (5, 204, 1)
    BASIC_06 = (6, 230, 1)
    BASIC_07 = (7, 268, 1)
    BASIC_08 = (8, 307, 1)
    BASIC_09 = (9, 324, 1)
    BASIC_10 = (10, 360, 1)
    BASIC_11 = (11, 396, 1)
    BASIC_12 = (12, 403, 1)

    VIP_01 = (1, 79, 15)
    VIP_02 = (2, 158, 15)
    VIP_03 = (3, 224, 15)
    VIP_04 = (4, 299, 15)
    VIP_05 = (5, 374, 15)
    VIP_06 = (6, 422, 15)
    VIP_07 = (7, 492, 15)
    VIP_08 = (8, 563, 15)
    VIP_09 = (9, 594, 15)
    VIP_10 = (10, 660, 15)
    VIP_11 = (11, 726, 15)
    VIP_12 = (12, 739, 15)

    LIFETIME = (999, 1688, 31)

    def __init__(self, month: int, price: int, access_bitmap: int):
        self.month = month
        self.price = price
        self.access_bitmap = access_bitmap

    @classmethod
    def from_price(cls, price) -> "SubscriptionPlanEnum":
        for item in cls:
            if item.price == price:
                return item
        raise ValueError(f"No subscription plan with price {price} found")
