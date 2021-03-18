# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import sqlite3
from sqlite3 import Error
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionDatabaseConnection(Action):

    def name(self) -> Text:
        return "action_database_connection"

    def run(self,dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text,Any]) -> List[Dict[Text, Any]]:

        conn = sqlite3.connect('/database/PrototypeDB.db')
        cur = conn.cursor()

        cur.execute('''CREATE TABLE requirements
               (requirement, categories, part)''')

        requirements = [
            ('the user should login with a registered email address and password','security,login,account,email,password','login window'),
            ('the user should be transferred from the login page to the landing page when the login is successful','usability,guide','login window,landing page'),
            ('the system should inform the user if the email address is not registered when the user is trying to login','usability,error','login window')
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

        conn.close()