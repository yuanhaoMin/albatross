from enum import Enum


class SubscriptionPlanEnum(Enum):
    BASIC_01 = (1, 34, 1)
    BASIC_02 = (2, 68, 1)
    BASIC_03 = (3, 96, 1)
    BASIC_04 = (4, 129, 1)
    BASIC_05 = (5, 161, 1)
    BASIC_06 = (6, 182, 1)
    BASIC_07 = (7, 212, 1)
    BASIC_08 = (8, 243, 1)
    BASIC_09 = (9, 256, 1)
    BASIC_10 = (10, 285, 1)
    BASIC_11 = (11, 313, 1)
    BASIC_12 = (12, 319, 1)

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
