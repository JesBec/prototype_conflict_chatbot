from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, EventType
#from rasa_core.channels.slack import SlackInput

import requests
import random
import sqlite3
from sqlite3 import Error

class ValidateCategoryForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_category_form"

    async def required_slots(self, slots_mapped_in_domain: List[Text], dispatcher: "CollectingDispatcher",tracker: "Tracker", domain: "DomainDict",
    ) -> Optional[List[Text]]:
        
        agreement = tracker.slots.get("agreement_on_categorization")
        intent = tracker.get_intent_of_latest_message()
        dispatcher.utter_message(text=f"Slot agreement_on_categorization: {intent}")
        if agreement == "/deny" and intent != "stop":
            additional_slots = ["agreement_on_categorization"]
            #dispatcher.utter_message(text=f"Agreement deny in required_slots")
            additional_slots.append("categorization_requirement_user")
                #dispatcher.utter_message(template="utter_select_categories_rasa")
            return additional_slots + slots_mapped_in_domain
        elif agreement == "/more_information_about_categories" and intent != "stop":
            additional_slots = ["agreement_on_categorization"]
            #dispatcher.utter_message(text=f"Agreement more info in required_slots")
            additional_slots.append("more_information_categories_needed")
            return additional_slots + slots_mapped_in_domain
        #elif tracker.get_intent_of_latest_message() == "stop" or tracker.get_intent_of_latest_message() == "deny":
        #    return {"action_deactivate_loop"}
        return slots_mapped_in_domain
        

    async def extract_agreement_on_categorization(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        
        #dispatcher.utter_message(text=f"Extract_agreement_on_categorization: {intent}")
        agreement = ""
        if tracker.get_intent_of_latest_message() == "affirm":
            agreement = tracker.get_intent_of_latest_message()
        elif tracker.get_intent_of_latest_message() == "deny":
            agreement = tracker.get_intent_of_latest_message()
            # Received input from a Slack interactive component of type 'multi_static_select', for which payload parsing is not yet supported.
        elif tracker.get_intent_of_latest_message() == "more_information_about_categories":
            agreement = tracker.get_intent_of_latest_message()
        else:
            agreement = tracker.get_slot("agreement_on_categorization") 

        return {"agreement_on_categorization": agreement}

    async def extract_categorization_requirement_user(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        #dispatcher.utter_message(text=f"extract_categorization_requirement_user")
        #intent = tracker.get_intent_of_latest_message()
        if tracker.get_intent_of_latest_message() == "deny":
            return {"categorization_requirement_user" : None}
        #dispatcher.utter_message(text=f"Extract Categorization requirement user (should be meeting+control): {intent}")
        return {"categorization_requirement_user" : tracker.get_intent_of_latest_message()}

    async def extract_more_information_categories_needed(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        #intent = tracker.get_intent_of_latest_message()
        #dispatcher.utter_message(text=f"extract_more_information_categories_needed (should be finished_checking_categories) and is: {intent}")
        if tracker.get_intent_of_latest_message() == "finished_checking_categories":
            return {"agreement_on_categorization" : None,"more_information_categories_needed" : False} # 
        return {"more_information_categories_needed" : None}

    def validate_part_of_system(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `part_of_system` value."""
        system_parts = ["link","meeting window","webpage","device"]
        slot_value_string = ""
        slot_value_string = slot_value

        part_of_system = slot_value_string.replace('_',' ')
        part_of_system = part_of_system.replace('/','')
        
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
        #intent = tracker.get_intent_of_latest_message()
        #dispatcher.utter_message(text=f"That is the intent of the new requirement: {intent}")
        return {"intent_new_requirement" : tracker.get_intent_of_latest_message()}
    
    def validate_more_information_categories_needed(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if tracker.get_slot("more_information_categories_needed") is False:
            return {"agreement_on_categorization" : None}
        return {"more_information_categories_needed" : tracker.get_slot("more_information_categories_needed")}

    #def validate_agreement_on_categorization(
    #    self,
    #    slot_value: Any,
    #    dispatcher: CollectingDispatcher,
    #    tracker: Tracker,
    #    domain: DomainDict,
    #) -> Dict[Text, Any]:
    #    if tracker.get_slot("more_information_categories_needed") is False:
    #        return {"agreement_on_categorization" : None}
    #    return {"agreement_on_categorization" : tracker.get_slot("agreement_on_categorization")}

class ValidateManageConflictForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_manage_conflict_form"

    async def required_slots(self, slots_mapped_in_domain: List[Text], dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: "DomainDict",
    ) -> Optional[List[Text]]:
        #agrees_with_conflict = tracker.get_slot("agrees_with_conflict")
        slots_append = ""
        if tracker.get_slot("does_participate") == True:
            additional_slots = ["does_participate"]
            additional_slots.append("agrees_with_conflict")
            #dispatcher.utter_message(text=f"does_participate is appended")

            if tracker.get_slot("agrees_with_conflict"):
                additional_slots.append("explanation_conflict")
            if tracker.get_slot("explanation_conflict"):
                additional_slots.append("preference")
            if tracker.get_slot("preference"):
                additional_slots.append("explanation_preference")
            if tracker.get_slot("explanation_preference") and HandleDatabase.conflict_detected == True:
                #dispatcher.utter_message("HandleDatabase.conflict_detected == True new slot when discovered")
                additional_slots.append("when_discovered")
                #return additional_slots + slots_mapped_in_domain
    
            return additional_slots + slots_mapped_in_domain
        elif tracker.get_slot("does_participate") == False:
                dispatcher.utter_message(text=f"Allright. Thank you for submitting your requirement. We will look into it as soon as possible.")
        
        return slots_mapped_in_domain

    def validate_does_participate(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        intent = tracker.get_intent_of_latest_message()
        does_participate = None
        if intent == "deny":
            does_participate = False
        elif intent == "affirm":
            does_participate = True
        #dispatcher.utter_message(text=f"validate_does_participate (should be deny or affirm): {does_participate}")
        return {"does_participate" : does_participate}

    async def extract_agrees_with_conflict(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        agrees = None
        #if tracker.get_slot("agrees_with_conflict"):
            #agrees = tracker.get_slot("agrees_with_conflict")
        if tracker.get_intent_of_latest_message() == "affirm":
            agrees = True
        elif tracker.get_intent_of_latest_message() == "deny":
            agrees = False
        return {"agrees_with_conflict" : True}

    async def extract_explanation_conflict(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        message = tracker.latest_message.get("text")
        #dispatcher.utter_message(text=f"extract explanation_conflict: {message}")
        return {"explanation_conflict" : tracker.latest_message.get("text")}

    async def extract_preference(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        message = tracker.latest_message.get("text")
        #dispatcher.utter_message("in extract preference: {message}")
        preference = None
        if tracker.get_slot("preference"):
            #dispatcher.utter_message("slot preference exists")
            preference = tracker.get_slot("preference")

        if "first" in message:
            #dispatcher.utter_message("in extract preference: first")
            preference = "first"
        elif "last" in message:
            preference = "last"
        return {"preference" : preference}

    async def extract_explanation_preference(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        message = tracker.latest_message.get("text")
        #dispatcher.utter_message(text=f"extract explanation_preference: {message}")
        return {"explanation_preference" : tracker.latest_message.get("text")}

    async def extract_when_discovered(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        message = tracker.latest_message.get("text")
        #dispatcher.utter_message(text=f"extract when_discovered: {message}")
        return {"when_discovered" : tracker.latest_message.get("text")}
       
class ValidateUserInformationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_user_information_form"
    
    def validate_does_participate_user(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]: 
        slot_value = None
        agrees = True
        #dispatcher.utter_message("in does participate_user")
        if tracker.get_intent_of_latest_message() == "deny":
            agrees = False
            slot_value = "not stated"
        return {"age" : slot_value, "main_use" : slot_value, "user_group" : slot_value, "does_participate_user" : agrees}

    


class ActionDatabase(Action):

    def name(self) -> Text:
         return "action_database"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        categories_requirement = None
        message_for_user = ""
        
        if tracker.get_slot("agreement_on_categorization") == "/affirm":
            categories_requirement = tracker.get_slot("intent_new_requirement")
            #dispatcher.utter_message(text=f"ADB affirm: {categories_requirement}")
        elif tracker.get_slot("agreement_on_categorization") == "/deny":
            categories_requirement = tracker.get_slot("categorization_requirement_user")
            #dispatcher.utter_message(text=f"ADB deny: {categories_requirement}")
     
        all_conflicting_categories = HandleDatabase.get_conflicting_categories(categories_requirement)
        #dispatcher.utter_message(text=f"all_conflicting_categories in ADB: {all_conflicting_categories}")
        
        #selected_conflict = HandleConflictManagement.select_conflict(tracker.get_slot("agreement_on_categorization"),
        #                                                             tracker.get_slot("intent_new_requirement"),
        #                                                             tracker.get_slot("categorization_requirement_user"),
        #                                                             tracker.get_slot("part_of_system"))
        
        
        conflicting_requirements = HandleDatabase.get_conflicting_requirements(all_conflicting_categories, 
                                                                               tracker.get_slot("part_of_system"))
        if conflicting_requirements is None:
            message_for_user = """We have checked your requirements for conflicts with other 
            requirements and there were non found.\n Great!\n But there are other requirements that need to be resolved."""
        else:
            message_for_user = """There was a conflict between your and already existing requirements.\n"""
        dispatcher.utter_message(text=f"{message_for_user}")


        selected_conflict = HandleConflictManagement.select_conflict(tracker.get_slot("intent_new_requirement"),
                                                                     tracker.get_slot("new_requirement"),
                                                                     tracker.get_slot("part_of_system"))
        message_conflict = "No conflict."
        if selected_conflict is not None:
            message_conflict = selected_conflict[0][1] + "with the category: " + selected_conflict[0][2] + " and " + selected_conflict[1][1] + " with the category: " + selected_conflict[1][2] 
        return [SlotSet("conflicting_requirements", message_conflict)]

class ActionSaveInformation(Action):
    def name(self) -> Text:
         return "action_save_information"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if HandleDatabase.conflict_detected == True:
            new_requirement_id = HandleDatabase.insert_new_requirement(tracker.get_slot("new_requirement"), 
                                                  tracker.get_slot("intent_new_requirement"), 
                                                  tracker.get_slot("categorization_requirement_user"), 
                                                  tracker.get_slot("part_of_system"), 
                                                  tracker.get_slot("when_discovered"))
            HandleConflictManagement.conflict_1_id = new_requirement_id
        #HandleDatabase.insert_conflicts_table(HandleDatabase.conflicting_requirements_and_ids, 
        #                                      tracker.get_slot("new_requirement"), 
        #                                      new_requirement_id, 
        #                                      tracker.get_slot("part_of_system"), 
        #                                      tracker.get_slot("explanation_conflict"), 
        #                                      "", 
        #                                      "")
        elif HandleConflictManagement.conflict_db_id is not None:
            HandleConflictManagement.update_conflict(tracker.get_slot("preference"),HandleConflictManagement.conflict_db_id)

        else:
            votes_requirement_1 = 0
            votes_requirement_2 = 0
            if tracker.get_slot("preference") == "first":
                votes_requirement_1 = 1
            elif  tracker.get_slot("preference") == "last":
                votes_requirement_2 = 1

            conflict_id = HandleConflictManagement.insert_conflict(HandleConflictManagement.conflict_1_id, #needs to be saved if conflicts from DB
                                                     HandleConflictManagement.conflict_2_id,#requirement_2_id, #needs
                                                     tracker.get_slot("agrees_with_conflict"), 
                                                     tracker.get_slot("explanation_conflict"), 
                                                     tracker.get_slot("part_of_system"), 
                                                     votes_requirement_1,#votes_requirement_1, #preference
                                                     votes_requirement_2,#votes_requirement_2, #preference
                                                     tracker.get_slot("explanation_preference"))

            #HandleConflictManagement.update_conflict_id(requirement_id, conflict_id)
        
        
        if tracker.get_slot("does_participate_user") == True:
            user_id = HandleConflictManagement.insert_user_information(tracker.get_slot("age"), 
                                                                   tracker.get_slot("main_use"), 
                                                                   tracker.get_slot("user_group"))
            HandleConflictManagement.update_requirement_user_id(user_id, new_requirement_id)

    

class HandleConflictManagement:
    #selected_conflicts_ids = []
    more_conflicts = False
    conflicting_requirements = []
    conflict_1_id = None
    conflict_2_id = None
    conflicts_from_db = []
    conflict_db_id = None

    #def select_conflict(agreement_on_categorization,categories_by_bot,categories_by_user,part_of_system)
    def select_conflict(category_new_requirement,new_requirement,part_of_system):
        text = None

        if not HandleConflictManagement.conflicting_requirements:
            HandleConflictManagement.conflicting_requirements = HandleDatabase.conflicting_requirements_and_ids

        #if agreement_on_categorization == "/affirm":
        #    all_conflicting_categories = HandleDatabase.get_conflicting_categories(categories_by_bot)  
        #    conflicting_requirements = HandleDatabase.get_conflicting_requirements(all_conflicting_categories, part_of_system)
        #elif agreement_on_categorization == "/deny":
        #    all_conflicting_categories = HandleDatabase.get_conflicting_categories(categories_by_user)  
        #    conflicting_requirements = HandleDatabase.get_conflicting_requirements(all_conflicting_categories, part_of_system)
        #chosen_conflict_1 = []
        conflicts =[]
        if HandleDatabase.conflict_detected == True:
            
            chosen_conflict_1 = [None, new_requirement, category_new_requirement]

            chosen_conflict_2 = []
            index = None
            if HandleConflictManagement.conflicting_requirements and len(HandleConflictManagement.conflicting_requirements) > 1:
                index = random.randint(0,len(HandleConflictManagement.conflicting_requirements)-1)
                chosen_conflict = HandleConflictManagement.conflicting_requirements[index]
                HandleConflictManagement.more_conflicts = True   
            elif HandleConflictManagement.conflicting_requirements and len(HandleConflictManagement.conflicting_requirements) == 1:
                index = 0
                chosen_conflict = HandleConflictManagement.conflicting_requirements[index]
                more_conflicts = False

            if chosen_conflict:
                HandleConflictManagement.conflict_2_id = chosen_conflict[0]
                chosen_conflict_2 = [chosen_conflict[0], chosen_conflict[1], chosen_conflict[2]]
        
            HandleConflictManagement.conflicting_requirements.pop(index)
            
            conflicts.append(chosen_conflict_1)
            conflicts.append(chosen_conflict_2)

        elif HandleDatabase.conflict_detected == False:
            if HandleConflictManagement.conflicts_from_db is None:
                HandleConflictManagement.conflicts_from_db = HandleConflictManagement.select_conflicts_to_resolve(part_of_system)
            if HandleConflictManagement.conflicts_from_db and len(HandleConflictManagement.conflicts_from_db) >= 1:
               if len(HandleConflictManagement.conflicts_from_db) > 1:
                   more_conflicts = True
               else:
                   more_conflicts = False
               index = random.randint(0,len(HandleConflictManagement.conflicts_from_db)-1)
               chosen_conflict = HandleConflictManagement.conflicts_from_db[index]
               HandleConflictManagement.conflict_db_id = chosen_conflict[0]
               conn = sqlite3.connect('./database/PrototypeDB.db')
               cur = conn.cursor()
               cur.execute('''SELECT rowid,* FROM requirements WHERE rowid = ? OR rowid = ?''', (chosen_conflict[1],chosen_conflict[2]))
               selected_conflicts = cur.fetchall()
               if selected_conflicts[0][6]:
                    conflict_1 = [selected_conflicts[0][0],selected_conflicts[0][1],selected_conflicts[0][6]]
               elif selected_conflicts[0][2]:
                    conflict_1 = [selected_conflicts[0][0],selected_conflicts[0][1],selected_conflicts[0][2]]
               if selected_conflicts[1][6]:
                    conflict_2 = [selected_conflicts[1][0],selected_conflicts[1][1],selected_conflicts[1][6]]
               elif selected_conflicts[1][2]:
                    conflict_2 = [selected_conflicts[1][0],selected_conflicts[1][1],selected_conflicts[1][2]]
          
               conflicts.append(conflict_1)
               conflicts.append(conflict_2)
               HandleConflictManagement.conflict_1_id = conflicts[0][0]
               HandleConflictManagement.conflict_1_id = conflicts[1][0]

        return conflicts
        

    def insert_conflict(requirement_1_id, requirement_2_id, user_agreed_conflict, reasoning_conflict, part_of_system, 
                        votes_requirement_1,votes_requirement_2,reasoning_preference):
        conn = sqlite3.connect('./database/PrototypeDB.db')
        cur = conn.cursor()

        cur.execute('INSERT INTO requirements_in_conflict VALUES (?,?,?,?,?,?,?,?)', (requirement_1_id, 
                                                                                      requirement_2_id,
                                                                                      user_agreed_conflict,
                                                                                      reasoning_conflict,
                                                                                      part_of_system, 
                                                                                      votes_requirement_1, 
                                                                                      votes_requirement_2,
                                                                                      reasoning_preference))
        conn.commit()
        conflict_id = cur.lastrowid
        
        return conflict_id

    #def update_conflict_id(requirement_id, conflict_id):
    #    conn = sqlite3.connect('./database/PrototypeDB.db')
    #    cur = conn.cursor()

    #    cur.execute('UPDATE requirements SET conflict_id = ? WHERE rowid = ?', (conflict_id,requirement_id,))
    #    conn.commit()
    
    def update_conflict(preference,rowid):
        conn = sqlite3.connect('./database/PrototypeDB.db')
        cur = conn.cursor()

        if preference == "first":
            cur.execute('UPDATE requirements_in_conflict SET votes_requirement_1 = votes_requirement_1 + 1 WHERE rowid = ?', (rowid,))
            conn.commit()
        elif preference == "last":
            cur.execute('UPDATE requirements_in_conflict SET votes_requirement_2 = votes_requirement_2 + 1 WHERE rowid = ?', (rowid,))
            conn.commit()

    def insert_user_information(age, main_use, user_group):
        conn = sqlite3.connect('./database/PrototypeDB.db')
        cur = conn.cursor()

        cur.execute('''INSERT INTO user_information VALUES (?,?,?)''', (age, main_use, user_group))
        conn.commit()

        return cur.lastrowid
    
    def update_requirement_user_id(user_id, new_requirement_id):
        conn = sqlite3.connect('./database/PrototypeDB.db')
        cur = conn.cursor()

        cur.execute('''UPDATE requirements SET user_id = ? WHERE rowid = ?''', (user_id, new_requirement_id))
        conn.commit()

    def select_conflicts_to_resolve(part_of_system):
        conn = sqlite3.connect('./database/PrototypeDB.db')
        cur = conn.cursor()

        cur.execute('SELECT rowid,* FROM requirements_in_conflict WHERE part_of_system = ?',(part_of_system,))
        return cur.fetchall()

    #def update_conflict_information(reasoning, votes_new_requirement, votes_requirement_in_conflict, row_id):
    #    conn = sqlite3.connect('./database/PrototypeDB.db')
    #    cur = conn.cursor()
    #    information = [reasoning, votes_new_requirement, votes_requirement_in_conflict, row_id]


class HandleDatabase:
    ids_of_conflicting_requirements = []
    conflicting_requirements_and_ids = []
    conflict_detected = False
    #conflicting_categories = []
    #requirements_and_ids = []
    
    def get_conflicting_categories(categories):
        conflicts = []
        conflicts.clear()
        conn = sqlite3.connect('./database/PrototypeDB.db')
        cur = conn.cursor()
      
        if categories:
            categories = categories.replace('+','_')
        else:
            categories = None

        cur.execute('SELECT categories_in_conflict FROM categories WHERE name = ?', (categories,))
        conflicts = cur.fetchall()
        if conflicts and conflicts[0][0].find(";"):
            conflicts = conflicts[0][0].split(';')
        else:
            conflicts = None

        conn.close()
        return conflicts

    def get_conflicting_requirements(all_conflicting_categories, part_of_system):
        HandleDatabase.conflicting_requirements_and_ids.clear()
        conn = sqlite3.connect('./database/PrototypeDB.db')
        cur = conn.cursor()
        
        
        if all_conflicting_categories and all_conflicting_categories[0] != "no conflict":
            all_conflicting_categories = all_conflicting_categories[0].split(';')
            for conflict in all_conflicting_categories:
                part_of_system = '%' + part_of_system + '%'
                conflict = '%' + conflict + '%'
                cur.execute('SELECT rowid,requirement,categories FROM requirements WHERE categories LIKE ? AND part LIKE ?', (conflict, part_of_system,))
                HandleDatabase.conflicting_requirements_and_ids = cur.fetchall()
                HandleDatabase.conflict_detected = True
        else:
            HandleDatabase.conflicting_requirements_and_ids = None
            HandleDatabase.conflict_detected = False


        conn.close()
        return HandleDatabase.conflicting_requirements_and_ids


    def insert_new_requirement(requirement, categories_by_chatbot, categories_by_user, part_of_system, where_found):
        conflict_id = None
        categories_approval = False
        status = "new"
        conn = sqlite3.connect('./database/PrototypeDB.db')
        cur = conn.cursor()
        
        cur.execute('INSERT INTO requirements VALUES(?,?,?,?,?,?,?,?,?,?)',(requirement,"NULL",part_of_system,status,categories_by_chatbot,categories_by_user,categories_approval,where_found,conflict_id, "NULL"))
        conn.commit()
        new_requirement_id = cur.lastrowid
        conn.close()
    
        #all_conflicting_categories = get_conflicting_categories(categories_by_user)
        #requirements_and_ids = get_conflicting_requirements(all_conflicting_categories, part_of_system)
        
        #insert_conflicts_table(HandleDatabase.conflicting_requirements_and_ids, requirement, new_requirement_id, part_of_system, "", "", "")

        return new_requirement_id

    # old way to put all conflicts into the table, that have not been evaluated by user
    def insert_conflicts_table(requirements_and_ids, new_requirement, new_requirement_id ,part_of_system, reasoning, votes_requirement_1, votes_requirement_2):
        #cur.execute('SELECT ROWID from requirements_by_users WHERE requirement = ?', (new_requirement,))
        #id_new_requirement = cur.fetchone()

        conn = sqlite3.connect('./database/PrototypeDB.db')
        cur = conn.cursor()

        #added_conflicting_requirements_ids = []
        new_conflicts = []
        for requirement_and_id in requirements_and_ids:
                    #added_conflicting_requirements_ids.append(requirement_and_id[0])
                    new_conflicts.append([new_requirement_id,requirement_and_id[0], part_of_system, reasoning, votes_requirement_1, votes_requirement_2])
    
        cur.executemany('INSERT INTO requirements_in_conflict VALUES (?,?,?,?,?,?,?,?)', (new_conflicts))
        conn.commit()

    #def select_conflict_to_resolve(new_requirement_id):
    #    #conflicting_requirements = []
    #    conn = sqlite3.connect('./database/PrototypeDB.db')
    #    cur = conn.cursor()
    #    cur.execute("SELECT rowid,requirement_1_id, requirement_2_id, part_of_system, reasoning, votes_requirement_1, votes_requirement_2 FROM requirements_in_conflict WHERE requirement_1_id=?", (new_requirement_id,))
    #    conflicting_requirements = cur.fetchall()
    #    rows = len(conflicting_requirements)

    #    index = 0
    #    if rows > 1:
    #        index = random.randint(0,rows-1)
 
    #    return conflicting_requirements[index]
    