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


def render(decision):
    print(decision.__doc__)
    for opt in decision.options.values():
        print(opt.hotkey, opt.name, opt.method.__doc__)

    choices = []
    finished = False
    while True:
        r = input(">")
        if r == 'exit':
            break
        if r not in decision.options:
            print("Try again")
            continue
        else:
            choices.append(r)
            if not decision.multiple:
                break


    return choices
