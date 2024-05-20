#!/usr/bin/python3
"""This section establishes the unit tests for the state.py module within models.

Unit test classes:
    TestStateInstantiation
    TestStateSave
    TestStateToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestStateInstantiation(unittest.TestCase):
    """Unit tests for verifying the instantiation of the State class."""

    def test_no_args_instantiates(self):
        self.assertEqual(State, type(State()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(State().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_class_attribute(self):
        state_instance = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(state_instance))
        self.assertNotIn("name", state_instance.__dict__)

    def test_two_states_unique_ids(self):
        first_state = State()
        second_state = State()
        self.assertNotEqual(first_state.id, second_state.id)

    def test_two_states_different_created_at(self):
        first_state = State()
        sleep(0.05)
        second_state = State()
        self.assertLess(first_state.created_at, second_state.created_at)

    def test_two_states_different_updated_at(self):
        first_state = State()
        sleep(0.05)
        second_state = State()
        self.assertLess(first_state.updated_at, second_state.updated_at)

    def test_str_representation(self):
        today_date = datetime.today()
        date_representation = repr(today_date)
        state_instance = State()
        state_instance.id = "123456"
        state_instance.created_at = state_instance.updated_at = today_date
        state_str = state_instance.__str__()
        self.assertIn("[State] (123456)", state_str)
        self.assertIn("'id': '123456'", state_str)
        self.assertIn("'created_at': " + date_representation, state_str)
        self.assertIn("'updated_at': " + date_representation, state_str)

    def test_args_unused(self):
        state_instance = State(None)
        self.assertNotIn(None, state_instance.__dict__.values())

    def test_instantiation_with_kwargs(self):
        today_date = datetime.today()
        iso_date = today_date.isoformat()
        state_instance = State(id="345", created_at=iso_date, updated_at=iso_date)
        self.assertEqual(state_instance.id, "345")
        self.assertEqual(state_instance.created_at, today_date)
        self.assertEqual(state_instance.updated_at, today_date)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestStateSave(unittest.TestCase):
    """Unit tests for verifying the save method of the State class."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        state_instance = State()
        sleep(0.05)
        first_updated_at = state_instance.updated_at
        state_instance.save()
        self.assertLess(first_updated_at, state_instance.updated_at)

    def test_two_saves(self):
        state_instance = State()
        sleep(0.05)
        first_updated_at = state_instance.updated_at
        state_instance.save()
        second_updated_at = state_instance.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        state_instance.save()
        self.assertLess(second_updated_at, state_instance.updated_at)

    def test_save_with_arg(self):
        state_instance = State()
        with self.assertRaises(TypeError):
            state_instance.save(None)

    def test_save_updates_file(self):
        state_instance = State()
        state_instance.save()
        state_id = "State." + state_instance.id
        with open("file.json", "r") as file:
            self.assertIn(state_id, file.read())


class TestStateToDict(unittest.TestCase):
    """Unit tests for verifying the to_dict method of the State class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        state_instance = State()
        self.assertIn("id", state_instance.to_dict())
        self.assertIn("created_at", state_instance.to_dict())
        self.assertIn("updated_at", state_instance.to_dict())
        self.assertIn("__class__", state_instance.to_dict())

    def test_to_dict_contains_added_attributes(self):
        state_instance = State()
        state_instance.middle_name = "Holberton"
        state_instance.my_number = 98
        self.assertEqual("Holberton", state_instance.middle_name)
        self.assertIn("my_number", state_instance.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        state_instance = State()
        state_dict = state_instance.to_dict()
        self.assertEqual(str, type(state_dict["id"]))
        self.assertEqual(str, type(state_dict["created_at"]))
        self.assertEqual(str, type(state_dict["updated_at"]))

    def test_to_dict_output(self):
        today_date = datetime.today()
        state_instance = State()
        state_instance.id = "123456"
        state_instance.created_at = state_instance.updated_at = today_date
        test_dict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': today_date.isoformat(),
            'updated_at': today_date.isoformat(),
        }
        self.assertDictEqual(state_instance.to_dict(), test_dict)

    def test_contrast_to_dict_dunder_dict(self):
        state_instance = State()
        self.assertNotEqual(state_instance.to_dict(), state_instance.__dict__)

    def test_to_dict_with_arg(self):
        state_instance = State()
        with self.assertRaises(TypeError):
            state_instance.to_dict(None)


if __name__ == "__main__":
    unittest.main()
