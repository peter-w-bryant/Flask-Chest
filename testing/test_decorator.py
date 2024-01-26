import unittest
from unittest.mock import MagicMock, patch

from flask import Flask, g
from flask_chest.decorator import flask_chest


class FlaskChestDecoratorTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

        # Dummy FlaskChest instance
        self.chest = MagicMock()
        self.chests = [self.chest]

        @self.app.route("/test")
        @flask_chest(chests=self.chests)
        def test_view():
            g.test_var = "Test Value"
            return "Test Response"

        self.client = self.app.test_client()

    def test_set_custom_request_id_default(self):
        with self.app.app_context():
            self.client.get("/test")
            self.assertEqual(type(g.custom_request_id), str)
            self.assertTrue(len(g.custom_request_id) > 0)
            self.assertTrue(len(g.custom_request_id) <= 255)

    def test_write_tracked_variables_default(self):
        with self.app.app_context():
            self.client.get("/test")
            self.chest.write.assert_called_once()

    def test_write_tracked_variables_default(self):
        with self.app.app_context():
            self.client.get("/test")


if __name__ == "__main__":
    unittest.main()
