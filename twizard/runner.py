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

from .tui import render
from .dsl import _DecisionMeta, Pop, Push

def start(decision, ctx=None, curses_win=None):
    if type(decision) is _DecisionMeta:
        decision = decision()
    if ctx is None:
        ctx = object()

    decision.ctx = ctx
    choices = render(decision)
    stack = [decision(choices)]

    state = None
    while stack:
        state = stack[-1].send(state)
        if isinstance(state, Push):
            choices = render(state.decision)
            stack.append(state.decision(choices))
            state = None
        elif isinstance(state, Pop):
            stack.pop()
            state = state.value

    return state


