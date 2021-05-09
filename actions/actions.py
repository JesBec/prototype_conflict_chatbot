from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet

import sqlite3
from sqlite3 import Error

class ValidateCategoryForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_category_form"

    def validate_part_of_system(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `part_of_system` value."""
        #dispatcher.utter_message(text=f"That is the slot value: {slot_value}")

        system_parts = ["link","meeting window","webpage","device"]
        slot_value_string = ""
        slot_value_string = slot_value

        part_of_system = slot_value_string.replace('_',' ')
        part_of_system = part_of_system.replace('/','')
        
        #print(f"First name given = {slot_value} length = {len(slot_value)}")
        if part_of_system not in system_parts:
            dispatcher.utter_message(text=f"This part does not exist in the system {part_of_system}.")
            return {"part_of_system": None}
        else:
            return {"part_of_system": part_of_system}

    def validate_new_requirement(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `new_requirement` value."""
        intent = tracker.get_intent_of_latest_message()
        #dispatcher.utter_message(text=f"That is the intent: {intent}")
        return {"intent_new_requirement" : intent}


    #async def extract_new_requirement(
    #    self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    #) -> Dict[Text, Any]:
    #     part_of_system = tracker.get_slot("new_requirement") 
    #     if part_of_system is not None:
    #       intent = tracker.get_intent_of_latest_message()
    #       dispatcher.utter_message(text=f"That is the intent: {intent}")
    #     return []

class ActionDatabase(Action):

    def name(self) -> Text:
         return "action_database"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent_new_requirement = tracker.get_slot("intent_new_requirement")
        #dispatcher.utter_message(text=f"Extracted intent: {intent_new_requirement}")
        #collected_intents = intent_new_requirement.split('+')
        all_conflicting_categories = HandleDatabase.get_conflicting_categories(intent_new_requirement)
        #dispatcher.utter_message(text=f"Conflicting catgeories: {all_conflicting_categories}")

        part_of_system = tracker.get_slot("part_of_system")
        conflicting_requirements_formatted = ""
        conflicting_requirements = HandleDatabase.get_conflicting_requirements(all_conflicting_categories, part_of_system)
        #dispatcher.utter_message(text=f"Conflicting requirements: {conflicting_requirements}")
        
        for requirement in conflicting_requirements:
            conflicting_requirements_formatted = conflicting_requirements_formatted + " " + requirement + "\n"
        return [SlotSet("conflicting_requirements", conflicting_requirements_formatted)]

class HandleDatabase:
    ids_of_conflicting_requirements = []
    conflicting_requirements = []
    conflict_detected = False
    #all_conflicting_categories = []
    #dispatcher.utter_message(text=f"Conflicting categories before method: {all_conflicting_categories}")

    def get_conflicting_categories(categories):
        conflicts = []
        conflicts.clear()
        conn = sqlite3.connect('./database/PrototypeDB.db')
        cur = conn.cursor()
        #print(categories)
        categories = categories.replace('+','_')
        cur.execute('SELECT ' + categories + ' from conflictingcategories')
        conflicts = cur.fetchone()

        #for category in categories:
           #category = category.replace('+','_')
           #cur.execute('SELECT ' + meeting+control + ' from conflictingcategories')
           #conflicts = cur.fetchone()
           #conflicts = conflicts[0].split("+")
           #for conflict in conflicts:
               #all_conflicting_categories.append(conflict)
        conn.close()
        print(f"Conflicting categories method: {conflicts}")
        return conflicts

    #ToDo just checking position 0 could lead to false results
    def get_conflicting_requirements(all_conflicting_categories, part_of_system):
        conflict_detected = False
        conn = sqlite3.connect('./database/PrototypeDB.db')
        cur = conn.cursor()
        HandleDatabase.conflicting_requirements.clear()
        all_conflicting_categories = all_conflicting_categories[0].split(';')
        if all_conflicting_categories[0] != "no conflict":
            for conflict in all_conflicting_categories:
                part_of_system = '%' + part_of_system + '%'
                conflict = '%' + conflict + '%'
                cur.execute('SELECT rowid,requirement FROM requirements WHERE categories LIKE ? AND part LIKE ?', (conflict, part_of_system,))
                requirements_and_ids = cur.fetchall()
                HandleDatabase.check_for_duplicting_conflicts(requirements_and_ids)

                conflict_detected = True
        else:
             conflict_detected = False

        conn.close()
        #print(f"Conflicting detected: {conflict_detected}")
        #dispatcher.utter_message(text=f"Conflicting detected: {conflict_detected}")
        return HandleDatabase.conflicting_requirements

    def check_for_duplicting_conflicts(requirements_and_ids):

        HandleDatabase.ids_of_conflicting_requirements.clear()
        if not HandleDatabase.ids_of_conflicting_requirements:
             for requirement_and_id in requirements_and_ids:
                  HandleDatabase.ids_of_conflicting_requirements.append(requirement_and_id[0])
                  HandleDatabase.conflicting_requirements.append(requirement_and_id[1])
        else:
             for requirement_and_id in requirements_and_ids:
                  if requirement_and_id[0] not in HandleDatabase.ids_of_conflicting_requirements:
                        HandleDatabase.conflicting_requirements.append(requirement_and_id[1])

    def insert_new_requirement(requirement, categories, part_of_system):
        conn = sqlite3.connect('./database/PrototypeDB.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO requirements VALUES(?,?,?)',(requirement,categories,part_of_system))
        conn.commit()
        conn.close()


class ActionHelloWorld(Action):

     def name(self) -> Text:
         return "action_hello_world"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message(text="Hello World!")
         try:
            conn = sqlite3.connect('./database/PrototypeDB.db')
         except Error as e:
           dispatcher.utter_message(text=e)

         part_of_system = tracker.get_slot("part_of_system") 

         if part_of_system is not null:
           dispatcher.utter_message(text=f"das ist drin: {part_of_system}")

         #cur = conn.cursor() 
        
         #cur.executemany('INSERT INTO requirements VALUES (?,?,?)',requirements)

         #conn.commit()
         conn.close()

         return []
