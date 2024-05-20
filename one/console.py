#!/usr/bin/python3
"""Command Line Interpreter"""
import cmd
import json
import re
import sys

from models import *
from models import storage


class HBNBCommand(cmd.Cmd):
    """Command Line Interpreter for HBNB Project"""

    prompt = "(hbnb)"

    def do_EOF(self, *args):
        """Exits the program."""
        print()
        return True

    def do_quit(self, *args):
        """Exits the program."""
        return True

    def do_create(self, line):
        """Creates an instance of the class."""
        if line != "" or line is not None:
            if line not in storage.classes():
                print("** class doesn't exist **")
            else:
                obj_instance = storage.classes()[line]()
                obj_instance.save()
                print(obj_instance.id)
        else:
            print("** class name missing **")

    def do_show(self, line):
        """Shows the instance details of the class."""
        if line == "" or line is None:
            print("** class name missing **")
        else:
            class_info = line.split(" ")
            if len(class_info) < 2:
                print("** instance id missing **")
            else:
                class_name = class_info[0]
                instance_id = class_info[1]
                if class_name in storage.classes():
                    key = f"{class_name}.{instance_id}"
                    if key not in storage.all():
                        print("** no instance found **")
                    else:
                        instance_dict = storage.all()[key]
                        print(instance_dict)
                else:
                    print("** class doesn't exist **")

    def do_destroy(self, line):
        """Deletes the instance of the class."""
        if line == "" or line is None:
            print("** class name missing **")
        else:
            class_info = line.split(" ")
            if len(class_info) < 2:
                print("** instance id missing **")
            else:
                class_name = class_info[0]
                instance_id = class_info[1]
                if class_name in storage.classes():
                    key = f"{class_name}.{instance_id}"
                    if key not in storage.all():
                        print("** no instance found **")
                    else:
                        del storage.all()[key]
                        storage.save()
                        return
                else:
                    print("** class doesn't exist **")

    def do_all(self, line):
        """Prints the string representation of all instances."""
        instance_obj = storage.all()
        instance_list = []

        if line == "" or line is None:
            for key, value in storage.all().items():
                instance_list.append(str(value))
            print(instance_list)
        else:
            if line not in storage.classes():
                print("** class doesn't exist **")
                return
            else:
                for key, value in storage.all().items():
                    class_name, instance_id = key.split(".")
                    if line == class_name:
                        instance_list.append(str(value))
                print(instance_list)

    def do_update(self, line):
        """Updates the instance of the class."""
        checks = re.search(r"^(\w+)\s([\S]+?)\s({.+?})$", line)
        if checks:
            class_name = checks.group(1)
            instance_id = checks.group(2)
            update_dict = checks.group(3)

            if class_name is None:
                print("** class name missing **")
            elif instance_id is None:
                print("** instance id missing **")
            elif update_dict is None:
                print("** attribute name missing **")
            else:
                if class_name not in storage.classes():
                    print("** class doesn't exist **")
                else:
                    key = f"{class_name}.{instance_id}"
                    if key not in storage.all():
                        print("** no instance found **")
                    else:
                        instance_dict = storage.all()[key]
                        update_dict = json.loads(update_dict)

                        attributes = storage.attributes()[class_name]
                        for key, value in update_dict.items():
                            if key in attributes:
                                value = attributes[key](value)
                                setattr(instance_dict, key, value)
                                storage.save()

        else:
            checks = re.search(
                r"^(\w+)\s([\S]+?)\s\"(.+?)\"\,\s\"(.+?)\"", line)
            class_name = checks.group(1)
            instance_id = checks.group(2)
            attribute = checks.group(3)
            value = checks.group(4)

            if class_name is None:
                print("** class name missing **")
            elif instance_id is None:
                print("** instance id missing **")
            elif attribute is None:
                print("** attribute name missing **")
            elif value is None:
                print("** value missing **")
            else:
                if class_name not in storage.classes():
                    print("** class doesn't exist **")
                else:
                    key = f"{class_name}.{instance_id}"
                    if key not in storage.all():
                        print("** no instance found **")
                    else:
                        instance_dict = storage.all()[key]
                        attributes_dict = storage.attributes()[class_name]
                        value = attributes_dict[attribute](value)
                        setattr(instance_dict, attribute, value)
                        storage.save()

    def emptyline(self):
        pass

    def precmd(self, line):
        if not sys.stdin.isatty():
            print()

        checks = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if checks:
            class_name = checks.group(1)
            command = checks.group(2)
            args = checks.group(3)

            if args is None:
                line = f"{command} {class_name}"
                return ''
            else:
                args_checks = re.search(r"^\"([^\"]*)\"(?:, (.*))?$", args)
                instance_id = args_checks[1]

                if args_checks.group(2) is None:
                    line = f"{command} {class_name} {instance_id}"
                else:
                    attribute_part = args_checks.group(2)
                    line = f"{command} {class_name} {instance_id} \
{attribute_part}"
                return ''

        return cmd.Cmd.precmd(self, line)

    def do_count(self, line):
        """Counts all the instances of the class."""
        count = 0
        for key in storage.all().keys():
            class_name, instance_id = key.split(".")
            if line == class_name:
                count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()

