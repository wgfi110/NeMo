# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2020 NVIDIA. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

from weakref import WeakSet


class ObjectRegistry(WeakSet):
    """
        Registry used for storing references to objects, generating unique names and monitoring their `uniqueness`.
    """

    def __init__(self, base_type_name):
        """ 
            Stores base type name.
        """
        super().__init__()
        self._base_type_name = base_type_name

    def register(self, new_obj, name):
        """
            Registers a new object using the provided name. 
            If name is none - generates new unique name.
            
            Args:
                new_obj: An object to be registered.
                name: A "proposition" of object name.
            
            Returns:
                A unique name (proposition or newly generated name).
        """

        # Check if object is already in a set.
        if new_obj in self:
            # Return its name.
            return new_obj.name

        # Check object name.
        if name is None:
            # Generate a new, unique name.
            unique_name = self.__generate_unique_name()
        else:
            # Check if name is unique.
            if self.has(name):
                raise NameError("A {} with name `{}` already exists!".format(self._base_type_name, name))
            # Ok, it is unique.
            unique_name = name

        # Finally, add object to the set.
        self.add(new_obj)

        # Return the name.
        return unique_name

    def has(self, name):
        """ Check if registry stores object with a given name. """
        for obj in self:
            if obj.name == name:
                return True
        # Else:
        return False

    def __generate_unique_name(self):
        """
            Generates a new unique name by adding postfix (number) to base name.

            Returns:
                A generated unique name.
        """
        # Iterate through numbers.
        postfix = 0
        while True:
            # Generate name.
            new_name = self._base_type_name + str(postfix)
            # Check uniqueneess.
            if not self.has(new_name):
                # Ok, got a unique name!
                break
            # Increment index.
            postfix += 1
        return new_name

    def __getitem__(self, key):
        """
        Object getter function.

        Args:
            key: Object name.

        Returns:
            Object associated with the key.
        """
        # Search for an object with a given name.
        for obj in self:
            # Retrieve object
            if obj.name == key:
                return obj
        # Else: seems that there is no object with that name.
        raise KeyError("A {} with name `{}` don't exists!".format(self._base_type_name, key))

    def __eq__(self, other):
        """ Checks if two registers have the same content. """
        if not isinstance(other, WeakSet):
            return False
        return super().__eq__(other)

    def summary(self):
        """ Returns a summary of objects on the list. """
        summary = "Objects:\n"
        for obj in self.items():
            summary += " * {} ({})\n".format(obj.name, type(obj).__name)
