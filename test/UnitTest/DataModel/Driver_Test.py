import unittest

from DataModel.Driver import Driver


class TestScore(unittest.TestCase):

    def test_driver_init(self):
        player_id = "123"
        driver = Driver(player_id)

        assert driver.get_player_id() == player_id
        assert driver.get_is_in_physical_vehicle() is False
        assert driver.get_score() == 0

    def test_driver_increase_score(self):
        player_id = "123"
        driver = Driver(player_id)

        driver.increase_score(10)
        assert driver.get_score() == 10

        driver.increase_score(5)
        assert driver.get_score() == 15

        driver.increase_score(-5)
        assert driver.get_score() == 10

    def test_driver_increase_score_margin_value(self):
        player_id = "123"
        driver = Driver(player_id)

        driver.increase_score(0)
        assert driver.get_score() == 0

        driver.increase_score(-5)
        assert driver.get_score() == 0

        driver.increase_score(1_000_000)
        assert driver.get_score() == 1_000_000

        driver.increase_score(5_000_000)
        assert driver.get_score() == 5_000_000
