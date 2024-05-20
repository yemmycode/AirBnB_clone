#!/usr/bin/python3
"""Module for testing the HBNBCommand Class"""

import unittest
from console import HBNBCommand
from unittest.mock import patch
from io import StringIO


class TestConsole(unittest.TestCase):
    """Test the HBNBCommand Console"""

    def test_help_command(self):
        """Test the help command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
        expected_output = """
Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update\n
"""
        self.assertEqual(expected_output, f.getvalue())

    def test_quit_command(self):
        """Test the quit command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("quit")
        msg = f.getvalue()
        self.assertTrue(len(msg) == 0)
        self.assertEqual("", msg)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("quit garbage")
        msg = f.getvalue()
        self.assertTrue(len(msg) == 0)
        self.assertEqual("", msg)

    def test_EOF_command(self):
        """Test the EOF command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("EOF")
        msg = f.getvalue()
        self.assertTrue(len(msg) == 1)
        self.assertEqual("\n", msg)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("EOF garbage")
        msg = f.getvalue()
        self.assertTrue(len(msg) == 1)
        self.assertEqual("\n", msg)

    def test_emptyline_command(self):
        """Test the emptyline command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("\n")
        msg = f.getvalue()
        self.assertTrue(len(msg) == 0)
        self.assertEqual("", msg)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("                     \n")
        msg = f.getvalue()
        self.assertTrue(len(msg) == 0)
        self.assertEqual("", msg)

    def test_do_all_command(self):
        """Test the do_all command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all")


if __name__ == "__main__":
    unittest.main()

