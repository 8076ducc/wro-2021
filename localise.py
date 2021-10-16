from pybricks.parameters import Color


class ParkingLot:
    def __init__(
        self,
        x: int,
        y: int,
        color: Color,
        barrier: bool,
        parked_color: Color,
        parked_type: int,
    ):
        self.x = x
        self.y = y
        self.color = color
        self.barrier = barrier
        self.parked_color = parked_color
        # 0: waiting, 1: parked
        self.parked_type = parked_type

    def update(self, parked_color: Color, parked_type: int, barrier: bool = None):
        self.parked_color = parked_color
        self.parked_type = parked_type
        if barrier != None:
            self.barrier = barrier


red_parking = [
    ParkingLot(2, 0, Color.RED, None, None, None),
    ParkingLot(1, 2, Color.RED, None, None, None),
    ParkingLot(0, 4, Color.RED, None, None, None),
    ParkingLot(1, 4, Color.RED, None, None, None),
]

green_parking = [
    ParkingLot(2, 0, Color.GREEN, None, None, None),
    ParkingLot(1, 2, Color.GREEN, None, None, None),
    ParkingLot(0, 4, Color.GREEN, None, None, None),
    ParkingLot(1, 4, Color.GREEN, None, None, None),
]

blue_parking = [
    ParkingLot(0, 0, Color.BLUE, None, None, None),
    ParkingLot(1, 0, Color.BLUE, None, None, None),
    ParkingLot(3, 2, Color.BLUE, None, None, None),
    ParkingLot(3, 4, Color.BLUE, None, None, None),
]


parking_lots = [
    blue_parking[0],
    blue_parking[1],
    red_parking[0],
    green_parking[0],
    green_parking[1],
    red_parking[1],
    green_parking[2],
    blue_parking[2],
    red_parking[2],
    red_parking[3],
    green_parking[3],
    blue_parking[3],
]


class ParkingBay:
    def __init__(
        self,
        # occupied: bool,
        # parked_color: Color,
    ):
        self.occupied = False
        self.parked_color = None

    def update(
        self,
        occupied: bool,
        parked_color: Color,
    ):
        self.occupied = occupied
        self.parked_color = parked_color


left_parking_bay = ParkingBay()
right_parking_bay = ParkingBay()


# def find_closest_parking(color: Color):


# def go_to(x: int, y: int):
