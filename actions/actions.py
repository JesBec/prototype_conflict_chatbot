# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

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
        
        print(f"First name given = {slot_value} length = {len(slot_value)}")
        if len(slot_value) <= 2:
            dispatcher.utter_message(text=f"That's a very short name. I'm assuming you mis-spelled.")
            return {"part_of_system": None}
        else:
            return {"part_of_system": slot_value}

    async def extract_account_security(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        intent = tracker.get_intent_of_latest_message()
        dispatcher.utter_message(text=f"That is the intent: {intent}")
        return []


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
         
         dispatcher.utter_message(text=f"das ist drin: {part_of_system}")

         #cur = conn.cursor() 
        
         #cur.executemany('INSERT INTO requirements VALUES (?,?,?)',requirements)

         #conn.commit()
         conn.close()

         return []


class ActionDatabaseConnection(Action):

    def name(self) -> Text:
         return "action_database_connection"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #conn = sqlite3.connect('/database/PrototypeDB.db')
        dispatcher.utter_message(text="Hello World!")

        #try:
        conn = sqlite3.connect('/database/PrototypeDB.db')
        #except Error as e:
            #dispatcher.utter_message(text = e)
            #print(e)

   

        cur = conn.cursor()

        cur.execute('''CREATE TABLE requirements
               (requirement, categories, part)''')

        requirements = [
            ('the user should login with a registered email address and password','security,login,account,email,password','login window'),
            ('the user should be transferred from the login page to the landing page when the login is successful','usability,guide','login window,landing page'),
            ('the system should inform the user if the email address is not registered when the user is trying to login','usability,error','login window'),
            ('the system should inform the user if the email address is incorrect when the user is trying to login','usability,error','login window'),
            ('the system should give the user the option to register a new account if the user tries to login and is not registered','security,login,account,error','login window'),
            ('the system should inform the user if the password is wrong when the user is trying to login','usability,error','login window'),
            ('the user should be able to reset the password if the user does not remember it','usability,error','login window'),
            ('the user can register a new account by adding a new email address and password','security,registration,password','registration window'),
            ('the system should transfer the user to the login page if the entered email address is already registered','usability,guide','registration window'),
            ('the system should not create a new account if another account already uses the same email address','security,account,email','registration window'),
            ('the system should store the password encrypted','security,password,encryption','data'),
            ('the user should create a password with at least 8 characters, a number, symbol, capital letter and lower-case letter','security,registration,password','data'),
            ('the system should disable login if 3 attempts to login have failed','security,login,access,error','login window')]
        
        cur.executemany('INSERT INTO stocks VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',requirements)

        cur.commit()
        #message = cur.fetchall()
        dispatcher.utter_message(text="geklappt")
        conn.close()

        return []