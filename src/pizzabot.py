import sys
from dataclasses import dataclass
from typing import List
import logging
import re
import math


def _l(msg: str): logging.getLogger('').info(msg)


def _e(msg: str): logging.getLogger('').error(msg)


def log_actions(actions: List['Action']):
    ...


@dataclass
class Location:
    x: int
    y: int


class FieldSize(Location):

    def __contains__(self, item) -> bool:
        if isinstance(item, Location):
            return item.y < self.y and item.x < self.x
        return False


class Action:
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    DROP_PIZZA = 0


class Task:
    raw: str

    pizzabot_location: Location
    houses_locations: List[Location]
    field_size: FieldSize

    VALID_ARG_REGEX = R'\dx\d [\(\d, \d\)]*'
    FIELD_SIZE_COORDINATES_REGEX = R'\dx\d'
    HOUSE_COORDINATES_REGEX = R'\(\d, \d\)'

    def __init__(self, raw_task: str):
        assert re.fullmatch(self.VALID_ARG_REGEX, raw_task)

        # 0, 0
        self.pizzabot_location = Location(x=0, y=0)

        # receiving houses coordinates from arg
        houses_coordinates = [
            coordinates[1:-1].split(', ')
            for coordinates in re.findall(self.HOUSE_COORDINATES_REGEX, raw_task)
        ]
        self.houses_locations = [
            Location(
                x=int(house_coordinates[0]),
                y=int(house_coordinates[1]),
            ) for house_coordinates in houses_coordinates
        ]

        # receiving field size from arg
        field_size: List[int] = re.findall(self.FIELD_SIZE_COORDINATES_REGEX, raw_task)[0].split('x')
        self.field_size = FieldSize(x=int(field_size[0]), y=int(field_size[1]))

        # checking does all of the provided houses are inside of the field
        for location in self.houses_locations:
            assert location in self.field_size


@dataclass
class PizzaBotRouter:
    bot_location: Location

    def build_route(self, houses_locations: List[Location]) -> List[Action]:
        sorted_houses_locations = self._sort_housings_locations(houses_locations)

        actions = []
        ...

    def _sort_housings_locations(self, houses_locations: List[Location]) -> List[Location]:
        sorted_locations = []
        lookup_location = self.bot_location

        for location in range(len(houses_locations)):
            closest_to_lookup = sorted(
                houses_locations,
                key=lambda l: math.fabs(l.x-lookup_location.x)+math.fabs(l.y-lookup_location.y),
            )[0]
            houses_locations.remove(closest_to_lookup)
            sorted_locations.append(closest_to_lookup)
            lookup_location = closest_to_lookup

        return sorted_locations


def proceed_input():
    raw_task = str(sys.argv[1])

    try:
        task = Task(raw_task)
    except Exception:  # noqa
        _e('Wrong argument provided, script must be executed in format: \n'
           'python pizzabot.py "{x0}x{y0} ({x1}, {y1}) ({x2}, {y...", - where:\n'
           '{x1}, {y1} - field size,\n'
           '{x1}, {y1} - house in need of pizza coordinates')
        return

    actions = PizzaBotRouter(task.pizzabot_location).build_route(task.houses_locations)
    log_actions(actions)


if __name__ == '__main__':
    proceed_input()
    exit()
