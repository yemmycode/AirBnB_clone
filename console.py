#!/usr/bin/python3
"""This module is the entry point for the command interpreter."""

import cmd
from models.base_model import BaseModel
from models import storage
import re
import json


class HBNBCommand(cmd.Cmd):
    """Defines the command interpreter class."""

    prompt = "(hbnb) "

    def default(self, line):
        """Handle unmatched commands."""
        self._precmd(line)

    def _precmd(self, line):
        """Intercept and handle class.syntax() formatted commands."""
        match = re.search(r"^(\w*)\.(\w+)\(([^)]*)\)$", line)
        if not match:
            return line
        
        classname, method, args = match.groups()
        match_uid_and_args = re.search(r'^"([^"]*)"(?:, (.*))?$', args)
        
        if match_uid_and_args:
            uid, attr_or_dict = match_uid_and_args.groups()
        else:
            uid, attr_or_dict = args, False

        attr_and_value = ""
        if method == "update" and attr_or_dict:
            match_dict = re.search(r'^({.*})$', attr_or_dict)
            if match_dict:
                self.update_dict(classname, uid, match_dict.group(1))
                return ""
            match_attr_and_value = re.search(r'^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if match_attr_and_value:
                attr_and_value = f"{match_attr_and_value.group(1) or ''} {match_attr_and_value.group(2) or ''}"
        
        command = f"{method} {classname} {uid} {attr_and_value}"
        self.onecmd(command.strip())
        return command

    def update_dict(self, classname, uid, s_dict):
        """Helper method for update() with a dictionary."""
        s = s_dict.replace("'", '"')
        d = json.loads(s)
        
        if not classname:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif not uid:
            print("** instance id missing **")
        else:
            key = f"{classname}.{uid}"
            if key not in storage.all():
                print("** no instance found **")
            else:
                attributes = storage.attributes()[classname]
                for attribute, value in d.items():
                    if attribute in attributes:
                        value = attributes[attribute](value)
                    setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()

    def do_EOF(self, line):
        """Handle the End Of File character."""
        print()
        return True

    def do_quit(self, line):
        """Exit the program."""
        return True

    def emptyline(self):
        """Do nothing on empty input."""
        pass

    def do_create(self, line):
        """Create a new instance of a class."""
        if not line:
            print("** class name missing **")
        elif line not in storage.classes():
            print("** class doesn't exist **")
        else:
            instance = storage.classes()[line]()
            instance.save()
            print(instance.id)

    def do_show(self, line):
        """Display the string representation of an instance."""
        if not line:
            print("** class name missing **")
        else:
            words = line.split()
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = f"{words[0]}.{words[1]}"
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, line):
        """Delete an instance by class name and id."""
        if not line:
            print("** class name missing **")
        else:
            words = line.split()
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = f"{words[0]}.{words[1]}"
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, line):
        """Print all instances, optionally filtered by class."""
        if line:
            words = line.split()
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                instances = [str(obj) for obj in storage.all().values() if type(obj).__name__ == words[0]]
                print(instances)
        else:
            instances = [str(obj) for obj in storage.all().values()]
            print(instances)

    def do_count(self, line):
        """Count the instances of a specified class."""
        words = line.split()
        if not words:
            print("** class name missing **")
        elif words[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            matches = [key for key in storage.all() if key.startswith(f"{words[0]}.")]
            print(len(matches))

    def do_update(self, line):
        """Update an instance's attribute by class name and id."""
        if not line:
            print("** class name missing **")
            return
        
        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(rex, line)
        if not match:
            print("** class name missing **")
            return
        
        classname, uid, attribute, value = match.groups()
        
        if classname not in storage.classes():
            print("** class doesn't exist **")
        elif not uid:
            print("** instance id missing **")
        else:
            key = f"{classname}.{uid}"
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                cast = None
                if not re.search(r'^".*"$', value):
                    cast = float if '.' in value else int
                else:
                    value = value.strip('"')
                
                attributes = storage.attributes()[classname]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass
                
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()

