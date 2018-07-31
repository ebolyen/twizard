# Copyright 2018 Evan Bolyen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import collections
import types

UnboundOption = collections.namedtuple(
    'UnboundOption', ['hotkey', 'name', 'method'])
Push = collections.namedtuple('Push', ['decision'])
Pop = collections.namedtuple('Pop', ['value'])


class _DecisionMeta(type):
    @classmethod
    def __prepare__(self, name, bases, multiple=False):
        return collections.OrderedDict()

    def __new__(cls, name, bases, dct, multiple=False):
        return type.__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct, multiple=False):
        # support inheritance
        lookup = collections.OrderedDict()
        if hasattr(cls, 'options'):
            lookup = cls.options.copy()

        # fix the decorated methods
        for key, value in dct.items():
            if type(value) is UnboundOption:
                if key in Decision.__dict__:
                    raise NameError("%r is a reserved method in Decision,"
                                    " it cannot be used as an option.")
                lookup[value.hotkey] = value
                dct[key] = value.method

        cls.multiple = multiple  # allow override by dct
        cls.options = lookup
        super(_DecisionMeta, cls).__init__(name, bases, dct)


class Decision(metaclass=_DecisionMeta):
    @classmethod
    def option(cls, hotkey, name=None):
        if name is None:
            name = method.__name__
        def decorator(method):
            # metaclass will re-associate this method with the class
            return UnboundOption(hotkey, name, method)
        return decorator

    def finalize(self):
        return None

    def get_default_selection(self):
        return []

    def yield_next(self):
        return
        yield

    def __call__(self, selected):
        if not hasattr(self, 'ctx'):
            self.ctx = object()

        for selection in selected:
            method = self.options[selection].method

            next_decisions = method(self)
            if not isinstance(next_decisions, types.GeneratorType):
                continue
            try:
                result = None
                while True:
                    decision = next_decisions.send(result)
                    if type(decision) is _DecisionMeta:
                        decision = decision()
                    decision.ctx = self.ctx
                    result = yield Push(decision)
            except StopIteration:
                pass

        next_decisions = self.yield_next()
        try:
            result = None
            while True:
                decision = next_decisions.send(result)
                if type(decision) is _DecisionMeta:
                    decision = decision()
                decision.ctx = self.ctx
                result = yield Push(decision)
        except StopIteration:
            pass

        yield Pop(self.finalize())

