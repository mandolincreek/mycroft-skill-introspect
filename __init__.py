# mycroft-skill-introspect - discover skills, intents, vocabulary, etc.
#
#    Copyright (C) 2018  Zachary T Welch <zach@mandolincreek.net>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
from mycroft.messagebus.message import Message

import re


def camel2words(name):
        return re.sub('(?!^)([A-Z][a-z]+)', r' \1', name)


class IntrospectSkill(MycroftSkill):
    def __init__(self):
        super(IntrospectSkill, self).__init__(name="IntrospectSkill")

    # Skill Introspection Intents

    @intent_handler(IntentBuilder(
                "CountSkillsIntent").require("Skill").require("Count"))
    def handle_skill_count(self, message):
        e = self.emitter
        msg = e.wait_for_response(Message("mycroft.skills.manifest"))

        n = len(msg.data.keys())
        self.speak_dialog("skill.count", data={"n_skill": n})

    @intent_handler(IntentBuilder(
                "ListSkillsIntent").require("Skill").require("List"))
    def handle_skill_list(self, message):
        e = self.emitter
        msg = e.wait_for_response(Message("mycroft.skills.manifest"))

        names = msg.data.values()
        for name in names:
            name = re.sub('Skill$', '', name)
            name = camel2words(name)
            self.speak(name)


def create_skill():
    return IntrospectSkill()

# vim: sw=4 sts=4 cindent et
