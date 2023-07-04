from enum import Enum


class SubscriptionPlanEnum(Enum):
    BASIC_01 = (1, 54, 1)
    BASIC_02 = (2, 108, 1)
    BASIC_03 = (3, 153, 1)
    BASIC_04 = (4, 204, 1)
    BASIC_05 = (5, 255, 1)
    BASIC_06 = (6, 288, 1)
    BASIC_07 = (7, 336, 1)
    BASIC_08 = (8, 384, 1)
    BASIC_09 = (9, 405, 1)
    BASIC_10 = (10, 450, 1)
    BASIC_11 = (11, 495, 1)
    BASIC_12 = (12, 504, 1)

    VIP_01 = (1, 180, 15)
    VIP_02 = (2, 360, 15)
    VIP_03 = (3, 510, 15)
    VIP_04 = (4, 680, 15)
    VIP_05 = (5, 850, 15)
    VIP_06 = (6, 960, 15)
    VIP_07 = (7, 1120, 15)
    VIP_08 = (8, 1280, 15)
    VIP_09 = (9, 1350, 15)
    VIP_10 = (10, 1500, 15)
    VIP_11 = (11, 1650, 15)
    VIP_12 = (12, 1680, 15)

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
