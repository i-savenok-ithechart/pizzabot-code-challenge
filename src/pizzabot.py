import sys
from dataclasses import dataclass
from typing import List
import logging
import re
import math


logging.basicConfig(level=logging.INFO, format="%(message)s")


def _l(msg: str): logging.getLogger('').info(msg)


def _e(msg: str): logging.getLogger('').error(msg)


@dataclass
class Location:
    x: int
    y: int


class LocationsList(list):

    def pop_closest(self, to: Location) -> Location:  # remove and return closest, raise if empty
        assert len(self), 'Empty'

        closest = sorted(
            self,
            key=lambda l: math.fabs(l.x-to.x)+math.fabs(l.y-to.y),
        )[0]
        self.remove(closest)
        return closest


class FieldSize(Location):

    def __contains__(self, item) -> bool:
        if isinstance(item, Location):
            return item.y <= self.y and item.x <= self.x
        return False


class Action:
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    DROP_PIZZA = 0

    DESCRIPTIONS = {
        UP: 'N: Move north',
        DOWN: 'S: Move south',
        LEFT: 'W: Move west',
        RIGHT: 'E: Move east',
        DROP_PIZZA: 'D: Drop pizza',
    }


class Task:
    pizzabot_location: Location = Location(0, 0)
    houses_locations: LocationsList
    field_size: FieldSize

    FIELD_SIZE_COORDINATES_REGEX = R'\d+x\d+'
    HOUSE_COORDINATES_REGEX = R'\s\(\d+\,\s\d+\)'
    VALID_ARG_REGEX = rf'{FIELD_SIZE_COORDINATES_REGEX}({HOUSE_COORDINATES_REGEX})+'

    def __init__(self, raw_task: str):
        assert re.fullmatch(self.VALID_ARG_REGEX, raw_task), 'Invalid argument format'  # validate arg format

        # receiving houses coordinates from arg
        houses_coordinates = [
            coordinates[2:-1].split(', ')
            for coordinates in re.findall(self.HOUSE_COORDINATES_REGEX, raw_task)
        ]
        self.houses_locations = LocationsList([
            Location(
                x=int(house_coordinates[0]),
                y=int(house_coordinates[1]),
            ) for house_coordinates in houses_coordinates
        ])

        # receiving field size from arg
        field_size: List[int] = re.findall(self.FIELD_SIZE_COORDINATES_REGEX, raw_task)[0].split('x')
        self.field_size = FieldSize(x=int(field_size[0]), y=int(field_size[1]))

        # checking does all of the provided houses are inside of the field
        for location in self.houses_locations:
            assert location in self.field_size, f'House ({location.x}, {location.y}) is ' \
                                                f'out of field {self.field_size.x}x{self.field_size.y}'


@dataclass
class PizzaBotRouter:
    bot_location: Location

    def build_route(self, houses_locations: LocationsList) -> List[int]:
        actions_codes = []

        for _ in range(len(houses_locations)):
            closest_location = houses_locations.pop_closest(self.bot_location)
            actions_codes += self.move_to(closest_location)
            actions_codes.append(Action.DROP_PIZZA)

        return actions_codes

    def move_to(self, location: Location) -> List[int]:  # change bot location to lookup, return list of actions codes
        actions_codes = []
        if location.x >= self.bot_location.x:
            actions_codes += [Action.RIGHT] * (location.x - self.bot_location.x)
        else:
            actions_codes += [Action.LEFT] * (self.bot_location.x - location.x)

        if location.y >= self.bot_location.y:
            actions_codes += [Action.UP] * (location.y - self.bot_location.y)
        else:
            actions_codes += [Action.DOWN] * (self.bot_location.y - location.y)

        self.bot_location.x, self.bot_location.y = location.x, location.y
        return actions_codes


def log_actions(actions_codes: List['int']):
    for code in actions_codes:
        _l(Action.DESCRIPTIONS[code])


def proceed_input():
    try:
        raw_task = str(sys.argv[1])
        task = Task(raw_task)
    except Exception as e:
        err_msg = f'({e})\n' if isinstance(e, AssertionError) else ''
        _e(f'{err_msg}'
           f'Wrong argument provided, script must be executed in format: \n'
           'python pizzabot.py "{x0}x{y0} ({x1}, {y1}) ({x2}, {y...", - where:\n'
           '{x1}, {y1} - field size,\n'
           '{x1}, {y1} - house in need of pizza coordinates')
        return

    actions = PizzaBotRouter(task.pizzabot_location).build_route(task.houses_locations)
    log_actions(actions)


if __name__ == '__main__':
    proceed_input()
    exit()
