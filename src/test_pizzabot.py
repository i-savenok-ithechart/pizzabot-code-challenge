import pytest

from pizzabot import Task, Location as L, FieldSize, PizzaBotRouter, LocationsList, Action as A


class TestPizzaBot:

    def test_init_task(self):
        t = Task("10x10 (5, 9) (0, 10) (1, 2)")
        assert (t.field_size.x, t.field_size.y) == (10, 10)
        assert (t.pizzabot_location.x, t.pizzabot_location.y) == (0, 0)
        assert t.houses_locations == [L(5, 9), L(0, 10), L(1, 2)]

        field_size = FieldSize(100, 110)
        houses_cords = [L(1, 2), L(3, 4), L(10, 3), L(100, 0)]
        t = Task(f"{field_size.x}x{field_size.y} {' '.join([f'({h.x}, {h.y})' for h in houses_cords])}")
        assert t.field_size == field_size
        assert t.houses_locations == houses_cords
        assert (t.pizzabot_location.x, t.pizzabot_location.y) == (0, 0)

    def test_validate_argument(self):
        valid_args = [
            '9x9 (1, 5) (0, 0) (9, 9)',
            '1x1 (1, 0) (0, 0) (1, 1)',
            '1000x1000 (1000, 0) (500, 345) (2, 19)',
        ]
        for valid_arg in valid_args:
            Task(valid_arg)

        invalid_args = [
            '1x1 (0,0)',
            '1x1 ',
            '1x1',
            '-1x1, (0, 0)',
            'axb, (0, 0)',
            '1x1 (0, 0)(0, 0)',
            'PizzaBot',
            '1x1, (-1, 0)',
            '1x1, (a, 0)',
            '1x1, (0.4, 0)',
            '1x1, (2, 0)',
            '1x1, (1, 2)',
        ]
        for invalid_arg in invalid_args:
            with pytest.raises(Exception):
                Task(invalid_arg)

    def test_pop_closest_from_locations_list(self):
        l0, l1, l2, l3, l4 = L(100, 100), L(5, 1), L(500, 20), L(6, 1), L(1, 4)
        locations_list = LocationsList([l1, l2, l3, l4])
        assert locations_list.pop_closest(l0) == l3
        assert locations_list.pop_closest(l0) == l1
        assert locations_list.pop_closest(l0) == l4
        assert locations_list.pop_closest(l0) == l2
        with pytest.raises(AssertionError):
            locations_list.pop_closest(l0)

    def test_router_move_to(self):
        r = PizzaBotRouter(L(10, 10))
        assert r.move_to(L(13, 10)) == [A.RIGHT, A.RIGHT, A.RIGHT]
        assert r.move_to(L(13, 7)) == [A.DOWN, A.DOWN, A.DOWN]
        assert r.move_to(L(10, 7)) == [A.LEFT, A.LEFT, A.LEFT]
        assert r.move_to(L(10, 10)) == [A.UP, A.UP, A.UP]

        assert r.move_to(L(12, 12)) == [A.RIGHT, A.RIGHT, A.UP, A.UP]
        assert r.move_to(L(10, 14)) == [A.LEFT, A.LEFT, A.UP, A.UP]
        assert r.move_to(L(8, 10)) == [A.LEFT, A.LEFT, A.DOWN, A.DOWN, A.DOWN, A.DOWN]

    def test_build_route(self):
        for locations, expected in [
            (
                [L(5, 5), L(1, 2), L(4, 1), L(0, 1), L(4, 3)],
                [
                    A.UP, A.DROP_PIZZA,  # 0, 0 -> 0, 1
                    A.RIGHT, A.UP, A.DROP_PIZZA,  # 0, 1 -> 1, 2
                    A.RIGHT, A.RIGHT, A.RIGHT, A.DOWN, A.DROP_PIZZA,  # 1, 2 -> 4, 1
                    A.UP, A.UP, A.DROP_PIZZA,  # 4, 1 -> 4, 3
                    A.RIGHT, A.UP, A.UP, A.DROP_PIZZA,  # 4, 3 -> 5, 5
                ],
            ),
            (
                [L(1, 1), L(1, 1), L(2, 2), L(2, 2), L(2, 2)],
                [A.RIGHT, A.UP, A.DROP_PIZZA, A.DROP_PIZZA, A.RIGHT, A.UP, A.DROP_PIZZA, A.DROP_PIZZA, A.DROP_PIZZA],
            ),
        ]:
            start_location = L(0, 0)
            r = PizzaBotRouter(start_location)
            assert r.build_route(LocationsList(locations)) == expected
