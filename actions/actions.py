from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import (SlotSet, EventType)

import requests
import random
import sqlite3
#import pymysql
#pymysql.install_as_MySQLdb()
import mysql.connector
#import MySQLdb
#from sqlite3 import Error

class ValidateCategoryForm(FormValidationAction):

    slots_to_reset = ["new_requirement",
    "intent_new_requirement",
    "conflicting_requirements",
    "x_agreement_on_categorization",
    "categorization_requirement_user",
    "more_information_categories_needed",
    "does_participate",
    "x_agrees_with_conflict",
    "explanation_conflict",
    "preference",
    "explanation_preference",
    "when_discovered",
    "does_participate_user",
    "z_age",
    "y_main_use",
    "x_user_group",
    "sub_category_audio",
    "sub_category_video",
    "sub_category_screensharing",
    "sub_category_recording",
    "sub_category_reaction",
    "sub_category_polling",
    "sub_category_livetranscript",
    "sub_category_chat",
    "requested_slot",
    "interruption",
    "ask_another_conflict"]
    req_categories = [
        "audio",
        "audio+option+microphone",
        "audio+option+screen",
        "audio+restriction",
        "audio+microphone+howto+start",
        "audio+microphone+howto+stop",
        "audio+screen+howto+start",
        "audio+screen+howto+stop",
        "audio+default",
        "audio+configation+option",
        "video",
        "video+option+camera",
        "video+option+screen",
        "video+screen+restriction",
        "video+screen+howto+stop",
        "video+screen+howto+start",
        "video+camera+howto+stop",
        "video+camera+howto+start",
        "video+default",
        "video+configuration",
        "screensharing+option",
        "screensharing+restriction+start",
        "screensharing+howto+stop",
        "screensharing+howto+start",
        "screensharing+default",
        "screensharing",
        "screensharing+restriction+windows",
        "screensharing+restriction+stop",
        "recording",
        "recording+restriction",
        "recording+howto+start",
        "recording+howto+stop",
        "recording+option",
        "recording+default",
        "reaction",
        "reaction+howto+start",
        "reaction+howto+stop",
        "reaction+default",
        "polling",
        "polling+restriction",
        "polling+howto+start",
        "polling+howto+stop",
        "polling+duration",
        "livetranscript",
        "livetranscript+restriction",
        "livetranscript+howto+start",
        "livetranscript+howto+stop",
        "livetranscript+default",
        "chat",
        "chat+howto+start",
        "chat+howto+stop",
        "chat+default"
    ]
 
    def name(self) -> Text:
        return "validate_category_form"

    async def required_slots(self, slots_mapped_in_domain: List[Text], dispatcher: "CollectingDispatcher",tracker: "Tracker", domain: "DomainDict",
    ) -> Optional[List[Text]]:
        agreement = tracker.slots.get("x_agreement_on_categorization")
        if tracker.slots.get("categorization_requirement_user"):
            category = tracker.slots.get("categorization_requirement_user")
            new_slot = "sub_category_" + category
            if new_slot != "sub_category_nocategory" and new_slot != "sub_category_changereq":
                additional_slots = ["categorization_requirement_user"]
                additional_slots.append(new_slot)
                return additional_slots + slots_mapped_in_domain

        if agreement == "/deny":
            additional_slots = ["x_agreement_on_categorization"]
            additional_slots.append("categorization_requirement_user")
            return additional_slots + slots_mapped_in_domain

        elif agreement == "/more_information_about_categories":
            additional_slots = ["x_agreement_on_categorization"]
            additional_slots.append("more_information_categories_needed")
            return additional_slots + slots_mapped_in_domain

        return slots_mapped_in_domain
        

    async def extract_x_agreement_on_categorization(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        agreement = ""
        if tracker.get_slot("x_agreement_on_categorization"):
            return {"x_agreement_on_categorization": tracker.get_slot("x_agreement_on_categorization")}
        elif tracker.get_intent_of_latest_message() == "affirm":
            agreement = tracker.get_intent_of_latest_message()
        elif tracker.get_intent_of_latest_message() == "deny":
            agreement = tracker.get_intent_of_latest_message()
        elif tracker.get_intent_of_latest_message() == "more_information_about_categories":
            agreement = tracker.get_intent_of_latest_message()
        else:
            agreement = tracker.get_slot("x_agreement_on_categorization")

        return {"x_agreement_on_categorization": agreement}

    async def extract_categorization_requirement_user(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        if tracker.get_intent_of_latest_message() == "deny":
            return {"categorization_requirement_user" : None}
        elif tracker.get_slot("categorization_requirement_user"):
            return {"categorization_requirement_user" : tracker.get_slot("categorization_requirement_user")}
        return {"categorization_requirement_user" : tracker.get_intent_of_latest_message()}

    async def extract_more_information_categories_needed(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        if tracker.get_intent_of_latest_message() == "finished_checking_categories":
            return {"x_agreement_on_categorization" : None, "more_information_categories_needed" : False}
        return {"more_information_categories_needed" : None}
    
    async def extract_sub_category_chat(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        if tracker.get_slot("sub_category_chat"):
            # if tracker.get_slot("sub_category_chat") == "goback":
            #     return { "categorization_requirement_user" : None, "sub_category_chat" : None}
            return {"sub_category_chat" : tracker.get_slot("sub_category_chat")}
        return {"sub_category_chat" : tracker.get_intent_of_latest_message()}
    
    async def extract_sub_category_livetranscript(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        if tracker.get_slot("sub_category_livetranscript"):
            return {"sub_category_livetranscript" : tracker.get_slot("sub_category_livetranscript")}
        return {"sub_category_livetranscript" : tracker.get_intent_of_latest_message()}

    async def extract_sub_category_polling(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        if tracker.get_slot("sub_category_polling"):
            return {"sub_category_polling" : tracker.get_slot("sub_category_polling")}
        return {"sub_category_polling" : tracker.get_intent_of_latest_message()}

    async def extract_sub_category_reaction(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        if tracker.get_slot("sub_category_reaction"):
            # if tracker.get_slot("sub_category_reaction") == "goback":
            #     return {"sub_category_reaction" : None, "categorization_requirement_user" : None}
            return {"sub_category_reaction" : tracker.get_slot("sub_category_reaction")}
        return {"sub_category_reaction" : tracker.get_intent_of_latest_message()}

    async def extract_sub_category_recording(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        if tracker.get_slot("sub_category_recording"):
            # if tracker.get_slot("sub_category_recording") == "goback":
            #     return {"sub_category_recording" : None, "categorization_requirement_user" : None}
            return {"sub_category_recording" : tracker.get_slot("sub_category_recording")}
        return {"sub_category_recording" : tracker.get_intent_of_latest_message()}

    async def extract_sub_category_screensharing(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        if tracker.get_slot("sub_category_screensharing"):
            # if tracker.get_slot("sub_category_screensharing") == "goback":
            #     return {"sub_category_screensharing" : None, "categorization_requirement_user" : None}
            return {"sub_category_screensharing" : tracker.get_slot("sub_category_screensharing")}
        return {"sub_category_screensharing" : tracker.get_intent_of_latest_message()}

    async def extract_sub_category_video(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        if tracker.get_slot("sub_category_video"):
            # if tracker.get_slot("sub_category_video") == "goback":
            #     return {"sub_category_video" : None, "categorization_requirement_user" : None}
            return {"sub_category_video" : tracker.get_slot("sub_category_video")}
        return {"sub_category_video" : tracker.get_intent_of_latest_message()}

    async def extract_sub_category_audio(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        if tracker.get_slot("sub_category_audio"):
            # if tracker.get_slot("sub_category_audio") == "goback":
            #     return {"sub_category_audio" : None, "categorization_requirement_user" : None}
            return {"sub_category_audio" : tracker.get_slot("sub_category_audio")}
        return {"sub_category_audio" : tracker.get_intent_of_latest_message()}

    def validate_new_requirement(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `new_requirement` value."""
        categorization_info = "no category found"
        if tracker.get_slot("requested_slot") == "new_requirement":
            #dispatcher.utter_message(tracker.get_intent_of_latest_message())
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. No requirement was submitted. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"new_requirement" : None}
            if tracker.get_intent_of_latest_message() == "explain":
                dispatcher.utter_message("Requirements explain the behaviour you want from our system. We need this information to see what you expect from our system. We will check if your requirement is in conflict with other requirements to see if we can implement it. If you would like to, I can tell you more about how to formulate a requirement.")
                return {"new_requirement" : None}
            if tracker.get_intent_of_latest_message() == "explain_how_to_requirement":
                dispatcher.utter_message("Here is an example of a requirement:\"The camera should be turned on when the meeting is started.\". Just try to be as precise as possible.")
                return {"new_requirement" : None}
            if tracker.get_intent_of_latest_message() in ValidateCategoryForm.req_categories:
                categorization_info = HandleDatabase.get_category_description(tracker.get_intent_of_latest_message())
        return {"intent_new_requirement" : tracker.get_intent_of_latest_message(), "categorization_info" : categorization_info}

    def validate_x_agreement_on_categorization(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        if tracker.get_slot("requested_slot") == "x_agreement_on_categorization":
            if tracker.get_slot("x_agreement_on_categorization") == "/changereq":
                dispatcher.utter_message("Of course. You can change it now.")
                return {"x_agreement_on_categorization" : None, "new_requirement" : None}
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. No requirement was submitted. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
        return {"x_agreement_on_categorization" : tracker.get_slot("x_agreement_on_categorization")}
    
    def validate_more_information_categories_needed(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if tracker.get_slot("requested_slot") == "more_information_categories_needed":
            if tracker.get_intent_of_latest_message() == "chitchat":
                return {"more_information_categories_needed" : None}
            if tracker.get_slot("more_information_categories_needed") is False:
                return {"x_agreement_on_categorization" : None}
        return {"more_information_categories_needed" : tracker.get_slot("more_information_categories_needed")}

    def validate_categorization_requirement_user(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        category = tracker.get_slot("categorization_requirement_user")
        if category is not None:
            sub_category = "sub_category_" + category
            if sub_category != "sub_category_changereq":
                if tracker.get_slot(sub_category) == "goback":
                    return {"categorization_requirement_user" : None, sub_category : None}
        if tracker.get_slot("requested_slot") == "categorization_requirement_user":
            if tracker.get_slot("categorization_requirement_user") == "changereq":
                dispatcher.utter_message("Of course. You can change it now.")
                return {"categorization_requirement_user" : None, "x_agreement_on_categorization" : None, "new_requirement" : None}
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. No requirement was submitted. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"categorization_requirement_user" : None}
            if tracker.get_intent_of_latest_message() == "explain":
                dispatcher.utter_message("We need a categorization of your requirement to check if it is conflicting with other requirements. We can only implement non-conflicting requirements.")
                return {"categorization_requirement_user" : None}
        return {"categorization_requirement_user" : tracker.get_slot("categorization_requirement_user")}


class ValidateManageConflictForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_manage_conflict_form"

    async def required_slots(self, slots_mapped_in_domain: List[Text], dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: "DomainDict",
    ) -> Optional[List[Text]]:
        if tracker.get_slot("does_participate") == True:
            additional_slots = ["does_participate"]
            if tracker.get_slot("x_agrees_with_conflict"):
                additional_slots.append("explanation_conflict")
            if tracker.get_slot("explanation_conflict"):
                additional_slots.append("preference")
            if tracker.get_slot("preference"):
                additional_slots.append("explanation_preference")
            if tracker.get_slot("explanation_preference") and HandleDatabase.conflict_detected == True:
                additional_slots.append("when_discovered")
            return additional_slots + slots_mapped_in_domain

        elif tracker.get_slot("does_participate") == False:
                dispatcher.utter_message(text=f"Allright. Thank you for submitting your requirement. We will look into it as soon as possible.")

        return slots_mapped_in_domain

    async def extract_explanation_conflict(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        explanation_conflict = tracker.get_slot("explanation_conflict")
        if tracker.get_slot("requested_slot") == "explanation_conflict":
            explanation_conflict = tracker.latest_message.get("text")
        return {"explanation_conflict" : explanation_conflict}

    async def extract_preference(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        #preference = None
        #if tracker.get_slot("requested_slot"):
        #    preference = tracker.get_slot("preference")
        return {"preference" : tracker.get_slot("preference")}

    async def extract_explanation_preference(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        return {"explanation_preference" : tracker.latest_message.get("text")}

    async def extract_when_discovered(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        return {"when_discovered" : tracker.latest_message.get("text")}

    def validate_does_participate(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        intent = tracker.get_intent_of_latest_message()
        does_participate = None
        if tracker.get_slot("requested_slot") == "does_participate":
            if intent == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"does_participate" : None}
            if intent == "explain":
                dispatcher.utter_message(text=f"Your information will help us to focus on the features you want. So it would be great if you could answer some questions.")
                return {"does_participate" : None}
            if intent == "stop":
                dispatcher.utter_message(text=f"Allright. We will stop asking questions. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "no_answer":
                dispatcher.utter_message("If you do not want to participate any more you can say no.")
                return {"does_participate_user" : None}
            if tracker.get_intent_of_latest_message() == "no_idea":
                dispatcher.utter_message("Should I explain to you why we ask you to participate? If you do not want to participate you can say no.")
                return {"does_participate_user" : None}
            elif intent == "deny":
                does_participate = False
                slot_value = "no answer"
            elif intent == "affirm":
                does_participate = True
                slot_value = None
        return {"does_participate" : does_participate, "x_agrees_with_conflict" : slot_value}

    def validate_x_agrees_with_conflict(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        #dispatcher.utter_message(tracker.get_slot("x_agrees_with_conflict"))
        if tracker.get_slot("requested_slot") == "x_agrees_with_conflict":
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"x_agrees_with_conflict" : None}
            if tracker.get_intent_of_latest_message() == "explain": 
                dispatcher.utter_message("We need your help to see if this is a real conflict. A conflict exists when two requirements cannot be implemented in the same system. E.g., they could contradict each other like \"camera on by default\" or \"camera off by default\". Sometimes constraints can hinder the implementation of requirements such as \"only the host can turn off the microphone of all participants\".")
                return {"x_agrees_with_conflict" : None}
            if tracker.get_intent_of_latest_message() == "no_idea": 
                dispatcher.utter_message("No problem. Should I explain to you why we ask this questions and what a conflict is? You can also skip this question if you tell me to.")
                return {"x_agrees_with_conflict" : None}
            if tracker.get_intent_of_latest_message() == "no_answer": 
                dispatcher.utter_message(text="Allright. It is fine if you do not want to answer this question. We will skip it then.")
                return {"x_agrees_with_conflict" : "no answer", "explanation_conflict" : "no answer"}
            if tracker.get_intent_of_latest_message() == "affirm":
                return {"x_agrees_with_conflict" : True}
            elif tracker.get_intent_of_latest_message() == "deny":
                return {"x_agrees_with_conflict" : False}
        return {"x_agrees_with_conflict" : tracker.get_slot("x_agrees_with_conflict")}

    def validate_explanation_conflict(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if tracker.get_slot("requested_slot") == "explanation_conflict":
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"explanation_conflict" : None}
            if tracker.get_intent_of_latest_message() == "explain":
                dispatcher.utter_message("Sometimes it is not so easy to decide if a conflict exists. Your information can help to figure this out. Maybe you do even have an idea how to get rid of the conflict.")
                return {"explanation_conflict" : None}
            if tracker.get_intent_of_latest_message() == "no_idea": 
                dispatcher.utter_message("No problem. Should I explain to you why we ask this questions? You can also skip this question if you tell me to.")
                return {"explanation_conflict" : None}
            if tracker.get_intent_of_latest_message() == "no_answer":
                 dispatcher.utter_message(text="Allright. It is fine if you do not want to answer this question. We will skip it then.")
                 return {"explanation_conflict" : "no answer"}
        return {"explanation_conflict" : tracker.get_slot("explanation_conflict")}

    def validate_preference(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if tracker.get_slot("requested_slot") == "preference":
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"preference" : None}
            if tracker.get_intent_of_latest_message() == "explain":
                dispatcher.utter_message("By telling us what you prefer, we can focus on the features that you find important since conflicting requirements can often not be implemented in the same system.")
                return {"preference" : None}
            if tracker.get_intent_of_latest_message() == "no_answer":
                dispatcher.utter_message(text="Allright. It is fine if you do not want to answer this question. We will skip it then.")
                return {"preference" : "no answer", "explanation_preference" : "no answer"}
            if tracker.get_intent_of_latest_message() == "no_idea": 
                dispatcher.utter_message("It is not always easy to make a decision. Should I explain to you why we ask this question? You can also skip this question if you tell me to?")
                return {"preference" : None}
            if tracker.get_intent_of_latest_message() == "first":
                return {"preference" : "first"}
            elif tracker.get_intent_of_latest_message() == "last":
                return {"preference" : "last"}
            elif tracker.get_intent_of_latest_message() == "they_do_the_same":
                return {"preference" : "they do the same", "explanation_preference" : "they do the same"}
            elif tracker.get_intent_of_latest_message() == "both":
                dispatcher.utter_message(text="I am sorry. You can only choose one.")
                return {"preference" : None}
        return {"preference" : tracker.get_slot("preference")}

    def validate_explanation_preference(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if tracker.get_slot("requested_slot") == "explanation_preference":
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"explanation_preference" : None}
            if tracker.get_intent_of_latest_message() == "explain":
                dispatcher.utter_message("Knowing exactly why you prefer one over the other or think why they are actually not conflicting will let us know what features our system needs to have to accomadate your needs.")
                return {"explanation_preference" : None}
            if tracker.get_intent_of_latest_message() == "no_idea": 
                dispatcher.utter_message("It is not always easy to explain a decision. Should I explain to you why we ask this question? You can also skip this question if you tell me to?")
                return {"explanation_preference" : None}
            if tracker.get_intent_of_latest_message() == "no_answer":
                dispatcher.utter_message(text="Allright. It is fine if you do not want to answer this question. We will skip it then.")
                return {"explanation_preference" : "no answer"}
            if tracker.get_slot("ask_another_conflict") == True:
                return {"interruption" : "ready save"}
        return {"explanation_preference" : tracker.get_slot("explanation_preference")}

    def validate_when_discovered(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if tracker.get_slot("requested_slot") == "when_discovered":
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"when_discovered" : None}
            if tracker.get_intent_of_latest_message() == "explain":
                dispatcher.utter_message("Asking you this will let us know which features you use and which have potential to get new features.")
                return {"when_discovered" : None}
            if tracker.get_intent_of_latest_message() == "no_answer":
                dispatcher.utter_message(text="Allright. It is fine if you do not want to answer. We will skip it then.")
                return {"when_discovered" : "no answer"}
            if tracker.get_intent_of_latest_message() == "no_idea": 
                dispatcher.utter_message("It is fine if you do not have an answer for this question. Just try to remember what you where doing on the system when your idea came to your mind. Should I explain to you why we ask this question? You can also skip this question if you tell me to.")
                return {"when_discovered" : None}
        return {"when_discovered" : tracker.get_slot("when_discovered")}

class ValidateAnotherConflictForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_another_conflict_form"



    async def required_slots(self, slots_mapped_in_domain: List[Text], dispatcher: "CollectingDispatcher", tracker: "Tracker", domain: "DomainDict",
    ) -> Optional[List[Text]]:
        if tracker.get_slot("does_participate") == True:
            additional_slots = ["does_participate"]
            if tracker.get_slot("x_agrees_with_conflict"):
                additional_slots.append("explanation_conflict")
            if tracker.get_slot("explanation_conflict"):
                additional_slots.append("preference")
            if tracker.get_slot("preference"):
                additional_slots.append("explanation_preference")
            if tracker.get_slot("explanation_preference") and HandleDatabase.conflict_detected == True:
                additional_slots.append("when_discovered")
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
        if tracker.get_slot("requested_slot") == "does_participate":
            if intent == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"does_participate" : None}
            if intent == "explain":
                dispatcher.utter_message(text=f"Your information will help us to focus on the features you want. So it would be great if you could answer some questions.")
                return {"does_participate" : None}
            if intent == "stop":
                dispatcher.utter_message(text=f"Allright. We will stop asking questions. No requirement was submitted. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "no_answer":
                dispatcher.utter_message("If you do not want to participate any more you can say no.")
                return {"does_participate_user" : None}
            if tracker.get_intent_of_latest_message() == "no_idea":
                dispatcher.utter_message("Should I explain to you why we ask you to participate? If you do not want to participate you can say no.")
                return {"does_participate_user" : None}
            elif intent == "deny":
                does_participate = False
                slot_value = "no answer"
            elif intent == "affirm":
                does_participate = True
                slot_value = None
        return {"does_participate" : does_participate, "x_agrees_with_conflict" : slot_value}

    async def extract_explanation_conflict(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        explanation_conflict = tracker.get_slot("explanation_conflict")
        if tracker.get_slot("requested_slot") == "explanation_conflict":
            explanation_conflict = tracker.latest_message.get("text")
        return {"explanation_conflict" : explanation_conflict}

    async def extract_preference(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        #preference = None
        #if tracker.get_slot("preference"):
        #    preference = tracker.get_slot("preference")
        return {"preference" : tracker.get_slot("preference")}

    async def extract_explanation_preference(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        return {"explanation_preference" : tracker.latest_message.get("text")}

    async def extract_when_discovered(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        return {"when_discovered" : tracker.latest_message.get("text")}

    def validate_x_agrees_with_conflict(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        #dispatcher.utter_message(tracker.get_slot("x_agrees_with_conflict"))
        if tracker.get_slot("requested_slot") == "x_agrees_with_conflict":
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"x_agrees_with_conflict" : None}
            if tracker.get_intent_of_latest_message() == "explain":
                dispatcher.utter_message("We need your help to see if this is a real conflict. A conflict exists when two requirements cannot be implemented in the same system. E.g., they could contradict each other like \"camera on by default\" or \"camera off by default\". Sometimes constraints can hinder the implementation of requirements such as \"only the host can turn off the microphone of all participants\".")
                return {"x_agrees_with_conflict" : None}
            if tracker.get_intent_of_latest_message() == "no_idea":
                dispatcher.utter_message("No problem. Should I explain to you why we ask this questions and what a conflict is? You can also skip this question if you tell me to.")
                return {"x_agrees_with_conflict" : None}
            if tracker.get_intent_of_latest_message() == "no_answer":
                dispatcher.utter_message(text="Allright. It is fine if you do not want to answer this question. We will skip it then.")
                return {"x_agrees_with_conflict" : "no answer", "explanation_conflict" : "no answer"}
            if tracker.get_intent_of_latest_message() == "affirm":
               return {"x_agrees_with_conflict" : True}
            elif tracker.get_intent_of_latest_message() == "deny":
               return {"x_agrees_with_conflict" : False}
        return {"x_agrees_with_conflict" : tracker.get_slot("x_agrees_with_conflict")}

    def validate_explanation_conflict(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if tracker.get_slot("requested_slot") == "explanation_conflict":
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"explanation_conflict" : None}
            if tracker.get_intent_of_latest_message() == "explain":
                dispatcher.utter_message("Sometimes it is not so easy to decide if a conflict exists. Your information can help to figure this out. Maybe you do even have an idea how to get rid of the conflict.")
                return {"explanation_conflict" : None}
            if tracker.get_intent_of_latest_message() == "no_idea":
                dispatcher.utter_message("No problem. Should I explain to you why we ask this questions? You can also skip this question if you tell me to.")
                return {"explanation_conflict" : None}
            if tracker.get_intent_of_latest_message() == "no_answer":
                dispatcher.utter_message(text="Allright. It is fine if you do not want to answer this question. We will skip it then.")
                return {"explanation_conflict" : "no answer"}
        return {"explanation_conflict" : tracker.get_slot("explanation_conflict")}

    def validate_preference(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if tracker.get_slot("requested_slot") == "preference":
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"preference" : None}
            if tracker.get_intent_of_latest_message() == "explain":
                dispatcher.utter_message("By telling us what you prefer, we can focus on the features that you find important since conflicting requirements can often not be implemented in the same system.")
                return {"preference" : None}
            if tracker.get_intent_of_latest_message() == "no_answer":
                dispatcher.utter_message(text="Allright. It is fine if you do not want to answer this question. We will skip it then.")
                return {"preference" : "no answer", "explanation_preference" : "no answer"}
            if tracker.get_intent_of_latest_message() == "no_idea":
                dispatcher.utter_message("It is not always easy to make a decision. Should I explain to you why we ask this question? You can also skip this question if you tell me to?")
                return {"preference" : None}
            if tracker.get_intent_of_latest_message() == "first":
                return {"preference" : "first"}
            elif tracker.get_intent_of_latest_message() == "last":
                return {"preference" : "last"}
            elif tracker.get_intent_of_latest_message() == "they_do_the_same":
                return {"preference" : "they do the same", "explanation_preference" : "they do the same"}
            elif tracker.get_intent_of_latest_message() == "both":
                dispatcher.utter_message(text="I am sorry. You can only choose one.")
                return {"preference" : None}
        return {"preference" : tracker.get_slot("preference")}

    def validate_explanation_preference(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if tracker.get_slot("requested_slot") == "explanation_preference":
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"explanation_preference" : None}
            if tracker.get_intent_of_latest_message() == "explain":
                dispatcher.utter_message("Knowing exactly why you prefer one over the other or think why they are actually not conflicting will let us know what features our system needs to have to accomadate your needs.")
                return {"explanation_preference" : None}
            if tracker.get_intent_of_latest_message() == "no_idea":
                dispatcher.utter_message("It is not always easy to explain a decision. Should I explain to you why we ask this question? You can also skip this question if you tell me to?")
                return {"explanation_preference" : None}
            if tracker.get_intent_of_latest_message() == "no_answer":
                dispatcher.utter_message(text="Allright. It is fine if you do not want to answer this question. We will skip it then.")
                return {"explanation_preference" : "no answer"}
            if tracker.get_slot("ask_another_conflict") == True:
                return {"interruption" : "ready save"}
        return {"explanation_preference" : tracker.get_slot("explanation_preference")}

    def validate_when_discovered(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if tracker.get_slot("requested_slot") == "when_discovered":
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"when_discovered" : None}
            if tracker.get_intent_of_latest_message() == "explain":
                dispatcher.utter_message("Asking you this will let us know which features you use and which have potential to get new features.")
                return {"when_discovered" : None}
            if tracker.get_intent_of_latest_message() == "no_answer":
                dispatcher.utter_message(text="Allright. It is fine if you do not want to answer. We will skip it then.")
                return {"when_discovered" : "no answer"}
            if tracker.get_intent_of_latest_message() == "no_idea":
                dispatcher.utter_message("It is fine if you do not have an answer for this question. Just try to remember what you where doing on the system when your idea came to your mind. Should I explain to you why we ask this question? You can also skip this question if you tell me to.")
                return {"when_discovered" : None}
        return {"when_discovered" : tracker.get_slot("when_discovered")}
       
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
        if tracker.get_slot("requested_slot") == "does_participate_user":
            if tracker.get_intent_of_latest_message() == "deny":
                agrees = False
                slot_value = "not stated"
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"does_participate_user" : None}
            if tracker.get_intent_of_latest_message() == "explain":
                dispatcher.utter_message("You do not have to participate. We will still save your requirement. Your additional information will help us to understand what you expect from our system.")
                return {"does_participate_user" : None}
            if tracker.get_intent_of_latest_message() == "no_answer":
                dispatcher.utter_message("If you do not want to answer personal questions you can say no.")
                return {"does_participate_user" : None}
            if tracker.get_intent_of_latest_message() == "no_idea": 
                dispatcher.utter_message("Should I explain to you why we ask you to participate? If you do not want to participate you can say no.")
                return {"does_participate_user" : None}
        return {"z_age" : slot_value, "y_main_use" : slot_value, "x_user_group" : slot_value, "does_participate_user" : agrees}

    def validate_z_age(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if tracker.get_slot("requested_slot") == "z_age":
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"z_age" : None}
            if tracker.get_intent_of_latest_message() == "explain":
                dispatcher.utter_message("We are only asking this to see if different user groups have different needs. You can choose to skip this question.")
                return {"z_age" : None}
            if tracker.get_intent_of_latest_message() == "no_answer":
                dispatcher.utter_message("You do not have to answer. We will skip this question.")
                return {"z_age" : "no answer"}
            if tracker.get_intent_of_latest_message() == "no_idea": 
                dispatcher.utter_message("Should I explain to you why we ask this question? You can also skip this question if you tell me to.")
                return {"z_age" : None}
        return {"z_age" : slot_value}

    def validate_y_main_use(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if tracker.get_slot("requested_slot") == "y_main_use":
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"y_main_use" : None}
            if tracker.get_intent_of_latest_message() == "explain":
                dispatcher.utter_message("If we know in which contexts the system gets used, we can work on adding features that will improve your experience.")
                return {"y_main_use" : None}
            if tracker.get_intent_of_latest_message() == "no_answer":
                dispatcher.utter_message("You do not have to answer. We will skip this question.")
                return {"y_main_use" : "no answer"}
            if tracker.get_intent_of_latest_message() == "no_idea": 
                dispatcher.utter_message("Should I explain to you why we ask this question? You can also skip this question if you tell me to.")
                return {"y_main_use" : None}
        return {"y_main_use" : slot_value}

    def validate_x_user_group(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if tracker.get_slot("requested_slot") == "x_user_group":
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"x_user_group" : None}
            if tracker.get_intent_of_latest_message() == "explain":
                dispatcher.utter_message("Knowing to which user group you belong will tell us to focus on features catering to the needs of this user group.")
                return {"x_user_group" : None}
            if tracker.get_intent_of_latest_message() == "no_answer":
                dispatcher.utter_message("You do not have to answer. We will skip this question.")
                return {"x_user_group" : "no answer"}
            if tracker.get_intent_of_latest_message() == "no_idea": 
                dispatcher.utter_message("Should I explain to you why we ask this question? You can also skip this question if you tell me to.")
                return {"x_user_group" : None}
        return {"x_user_group" : slot_value}


class ActionDatabase(Action):
    categories_requirement = None
    #round = 0
    sub_categories = ["sub_category_audio",
                      "sub_category_video",
                      "sub_category_screensharing",
                      "sub_category_recording",
                      "sub_category_reaction",
                      "sub_category_polling",
                      "sub_category_livetranscript",
                      "sub_category_chat"]
    possible_categories = []

    def name(self) -> Text:
         return "action_database"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            message_for_user = ""
        
            if tracker.get_slot("x_agreement_on_categorization") == "/affirm":
                ActionDatabase.categories_requirement = tracker.get_slot("intent_new_requirement")
         
            elif tracker.get_slot("x_agreement_on_categorization") == "/deny":
                ActionDatabase.categories_requirement = tracker.get_slot("categorization_requirement_user")
                for sub_category in ActionDatabase.sub_categories:
                    if tracker.get_slot(sub_category) is not None:
                        ActionDatabase.categories_requirement = tracker.get_slot(sub_category)
     
            all_conflicting_categories = HandleDatabase.get_conflicting_categories(ActionDatabase.categories_requirement)
            conflicting_requirements = HandleDatabase.get_conflicting_requirements(all_conflicting_categories)

            selected_conflict = HandleConflictManagement.select_conflict(ActionDatabase.categories_requirement,
                                                                         tracker.get_slot("new_requirement"))

            if conflicting_requirements is None:
                message_for_user = """We have checked your requirements for conflicts with other requirements and there were non found.\n Great!\n But there are other requirement conflicts that need to be resolved."""
            elif tracker.get_slot("categorization_requirement_user") == "nocategory":
                message_for_user = """Since your requirement does not fit any of our predefined requirements we cannot check if it is conflicting with any other requirements, yet. \n But there are other requirement conflicts that need to be resolved."""
            else:
                message_for_user = """There was a conflict between your and already existing requirements.\n"""
            dispatcher.utter_message(text=f"{message_for_user}")

            if selected_conflict:
                #message_conflict = "\" " + selected_conflict[0][1] + "\" (" + selected_conflict[0][2] + ") and \"" + selected_conflict[1][1] + "\" (" + selected_conflict[1][2] +")"
                message_conflict = "\"" + selected_conflict[0][1] + "\"" + " and \"" + selected_conflict[1][1] + "\""
            else:
                message_conflict = "No conflict found."
        
            #ActionDatabase.round = 1
            return [SlotSet("conflicting_requirements", message_conflict)]


class ActionSaveRequirement(Action):
    def name(self) -> Text:
        return "action_save_requirement"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.get_slot("new_requirement") and tracker.get_slot("intent_new_requirement"):
            category_new_requirement = tracker.get_slot("intent_new_requirement")
            if ActionDatabase.categories_requirement is not None:
                category_new_requirement = ActionDatabase.categories_requirement

            ActionSaveFirstConflict.new_requirement_id = HandleDatabase.insert_new_requirement(tracker.get_slot("new_requirement"),
                                                                                               category_new_requirement,
                                                                                               ActionDatabase.categories_requirement,
                                                                                               "no answer")


class ActionSaveInformation(Action):
    user_id = None
    def name(self) -> Text:
         return "action_save_information"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        votes_requirement_1 = 0
        votes_requirement_2 = 0
        if tracker.get_slot("preference") == "first":
            votes_requirement_1 = 1
        elif tracker.get_slot("preference") == "last":
            votes_requirement_2 = 1

        conflict_id = HandleConflictManagement.insert_conflict(HandleConflictManagement.conflict_1_id, #needs to be saved if conflicts from DB
                                                    HandleConflictManagement.conflict_2_id,#requirement_2_id, #needs
                                                    tracker.get_slot("x_agrees_with_conflict"),
                                                    tracker.get_slot("explanation_conflict"), 
                                                    votes_requirement_1,
                                                    votes_requirement_2,
                                                    tracker.get_slot("explanation_preference"))

        if tracker.get_slot("does_participate_user") == True and ActionSaveInformation.user_id is None:
            ActionSaveInformation.user_id = HandleConflictManagement.insert_user_information(tracker.get_slot("z_age"),
                                                                    tracker.get_slot("y_main_use"),
                                                                    tracker.get_slot("x_user_group"))
            HandleConflictManagement.update_requirement_user_id(ActionSaveInformation.user_id, ActionSaveFirstConflict.new_requirement_id)

        #HandleDatabase.conflict_detected == False
        #SlotSet("ask_another_conflict", True)

        print("Information was saved.<")

        return [SlotSet(slot, None) for slot in ValidateCategoryForm.slots_to_reset]


class ActionSaveFirstConflict(Action):
    user_id = None
    second_round = False
    new_requirement_id = None
    conflict_id = None
    reset_mgmt_form = ["does_participate",
                        "x_agrees_with_conflict",
                        "explanation_conflict",
                        "preference",
                        "explanation_preference",
                        "when_discovered"]

    def name(self) -> Text:
         return "action_save_first_conflict"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot("new_requirement") and tracker.get_slot("intent_new_requirement") and ActionSaveFirstConflict.second_round == False:

            category_new_requirement = tracker.get_slot("intent_new_requirement")
            if ActionDatabase.categories_requirement is not None:
                category_new_requirement = ActionDatabase.categories_requirement

            ActionSaveFirstConflict.new_requirement_id = HandleDatabase.insert_new_requirement(tracker.get_slot("new_requirement"), 
                                                      category_new_requirement, 
                                                      ActionDatabase.categories_requirement, 
                                                      tracker.get_slot("when_discovered"))

            if HandleDatabase.conflict_detected == True:
                HandleConflictManagement.conflict_1_id = ActionSaveFirstConflict.new_requirement_id
        
            #elif HandleConflictManagement.conflict_db_id is not None: #### really update or new entry in DB?
            #    HandleConflictManagement.update_conflict(tracker.get_slot("preference"),HandleConflictManagement.conflict_db_id)

            else:
                votes_requirement_1 = 0
                votes_requirement_2 = 0
                if tracker.get_slot("preference") == "first":
                    votes_requirement_1 = 1
                elif tracker.get_slot("preference") == "last":
                    votes_requirement_2 = 1

                ActionSaveFirstConflict.conflict_id = HandleConflictManagement.insert_conflict(HandleConflictManagement.conflict_1_id, #needs to be saved if conflicts from DB
                                                         HandleConflictManagement.conflict_2_id,#requirement_2_id, #needs
                                                         tracker.get_slot("x_agrees_with_conflict"),
                                                         tracker.get_slot("explanation_conflict"), 
                                                         votes_requirement_1,
                                                         votes_requirement_2,
                                                         tracker.get_slot("explanation_preference"))

            print("First requirement saved.")
            HandleDatabase.conflict_detected = False
            ActionSaveFirstConflict.second_round = True

            selected_conflict = HandleConflictManagement.select_conflict(ActionDatabase.categories_requirement,
                                                                         tracker.get_slot("new_requirement"))

            if selected_conflict:
                message_conflict = "\"" + selected_conflict[0][1] + "\"" + " and \"" + selected_conflict[1][1] + "\""
            else:
                message_conflict = "No conflict found."

            return [SlotSet("does_participate", None),
                    SlotSet("x_agrees_with_conflict", None),
                    SlotSet("explanation_conflict", None),
                    SlotSet("preference", None),
                    SlotSet("explanation_preference", None),
                    SlotSet("when_discovered", None),
                    SlotSet("ask_another_conflict", True),
                    SlotSet("conflicting_requirements", message_conflict)]
        print("First requirement NOT saved.")
        #return

    

class HandleConflictManagement:
    more_conflicts = False
    conflicting_requirements = []
    conflict_1_id = None
    conflict_2_id = None
    conflicts_from_db = []
    conflict_db_id = None
    mydb = mysql.connector.connect(host='35.246.207.244',
                                   user='root',
                                   password='d0NK3yK0ng',
                                   db='Chatbot')


    def select_conflict(category_new_requirement, new_requirement):
        text = None
        conflicts = []
        conflict_information_found = False
        print("Conflict detected")
        print(HandleDatabase.conflict_detected)
        print("Saved conflicts in array")
        print(conflicts)
        mydb = mysql.connector.connect(host='35.246.207.244',
                                       user='root',
                                       password='d0NK3yK0ng',
                                       db='Chatbot')
        if HandleDatabase.conflict_detected == True:
            if not HandleConflictManagement.conflicting_requirements:
                print(HandleDatabase.conflicting_requirements_and_ids)
                HandleConflictManagement.conflicting_requirements = HandleDatabase.conflicting_requirements_and_ids
            
            chosen_conflict_1 = [None, new_requirement, category_new_requirement]
            chosen_conflict_2 = []
            index = None

            if HandleConflictManagement.conflicting_requirements and len(HandleConflictManagement.conflicting_requirements) > 1:
                index = random.randint(0,len(HandleConflictManagement.conflicting_requirements)-1)
                HandleConflictManagement.more_conflicts = True   
            elif HandleConflictManagement.conflicting_requirements and len(HandleConflictManagement.conflicting_requirements) == 1:
                index = 0
                HandleConflictManagement.more_conflicts = False

            chosen_conflict = HandleConflictManagement.conflicting_requirements[index]

            if chosen_conflict:
                HandleConflictManagement.conflict_2_id = chosen_conflict[9]
                chosen_conflict_2 = [chosen_conflict[9], chosen_conflict[0], chosen_conflict[1]]
        
            HandleConflictManagement.conflicting_requirements.pop(index)
            print("HandleConflictManagement.conflicting_requirements")
            print(HandleConflictManagement.conflicting_requirements)
            
            conflicts.append(chosen_conflict_1)
            conflicts.append(chosen_conflict_2)

        elif HandleDatabase.conflict_detected == False:
      
            if not HandleConflictManagement.conflicts_from_db:
               HandleConflictManagement.conflicts_from_db = HandleConflictManagement.select_conflicts_to_resolve()
               
            if HandleConflictManagement.conflicts_from_db and len(HandleConflictManagement.conflicts_from_db) >= 1:
               
               if len(HandleConflictManagement.conflicts_from_db) > 1:
                   HandleConflictManagement.more_conflicts = True
               else:
                   HandleConflictManagement.more_conflicts = False
               index = random.randint(0, len(HandleConflictManagement.conflicts_from_db)-1)
               chosen_conflict = HandleConflictManagement.conflicts_from_db[index]
               HandleConflictManagement.conflicts_from_db.pop(index)
               HandleConflictManagement.conflict_db_id = chosen_conflict[0]

               #conn = sqlite3.connect('./database/PrototypeDB.db')
               cur = mydb.cursor()
               cur.execute('''SELECT * FROM requirements WHERE requirementID = %s OR requirementID = %s''', (chosen_conflict[0],chosen_conflict[1]))
               selected_conflicts_db = cur.fetchall()

               if selected_conflicts_db and selected_conflicts_db is not None:
                                #id
                   conflict_1 = [selected_conflicts_db[0][9],selected_conflicts_db[0][0],selected_conflicts_db[0][1]]
                   conflict_2 = [selected_conflicts_db[1][9],selected_conflicts_db[1][0],selected_conflicts_db[1][1]]
                   conflicts.append(conflict_1)
                   conflicts.append(conflict_2)
                   HandleConflictManagement.conflict_1_id = selected_conflicts_db[0][9]
                   HandleConflictManagement.conflict_2_id = selected_conflicts_db[1][9]

        mydb.close()
        return conflicts
        

    def insert_conflict(requirement_1_id, requirement_2_id, user_agreed_conflict, reasoning_conflict, 
                        votes_requirement_1,votes_requirement_2,reasoning_preference):
        mydb = mysql.connector.connect(host='35.246.207.244',
                                       user='root',
                                       password='d0NK3yK0ng',
                                       db='Chatbot')
        cur = mydb.cursor()

        cur.execute('''INSERT INTO requirements_in_conflict (requirement_1_id,
                                                             requirement_2_id,
                                                             user_agreement_conflict,
                                                             reasoning_conflict,
                                                             votes_requirment_1,
                                                             votes_requirement_2,
                                                             reasoning_preference,
                                                             status) 
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s)''', (requirement_1_id,
                                                              requirement_2_id,
                                                              user_agreed_conflict,
                                                              reasoning_conflict,
                                                              votes_requirement_1,
                                                              votes_requirement_2,
                                                              reasoning_preference,
                                                              "new"))
        mydb.commit()
        conflict_id = cur.lastrowid
        mydb.close()
        return conflict_id
    
    def update_conflict(preference,rowid):
        mydb = mysql.connector.connect(host='35.246.207.244',
                                       user='root',
                                       password='d0NK3yK0ng',
                                       db='Chatbot')
        cur = mydb.cursor()

        if preference == "first":
            cur.execute('UPDATE requirements_in_conflict SET votes_requirment_1 = 1, votes_requirement_2 = 0 WHERE conflictID = %s', (rowid,))
            mydb.commit()
        elif preference == "last":
            cur.execute('UPDATE requirements_in_conflict SET votes_requirement_1 = 0, votes_requirement_2 = 1 WHERE conflictID = %s', (rowid,))
            mydb.commit()
        mydb.close()

    def insert_user_information(age, main_use, user_group):
        mydb = mysql.connector.connect(host='35.246.207.244',
                                       user='root',
                                       password='d0NK3yK0ng',
                                       db='Chatbot')
        cur = mydb.cursor()

        cur.execute('''INSERT INTO user_information (age,main_use,user_group) VALUES (%s,%s,%s)''', (age, main_use, user_group))
        mydb.commit()
        user_id = cur.lastrowid
        mydb.close()

        return user_id
    
    def update_requirement_user_id(user_id, new_requirement_id):
        mydb = mysql.connector.connect(host='35.246.207.244',
                                       user='root',
                                       password='d0NK3yK0ng',
                                       db='Chatbot')
        cur = mydb.cursor()

        cur.execute('''UPDATE requirements SET user_id = %s WHERE requirementID = %s''', (user_id, new_requirement_id))
        mydb.commit()
        mydb.close()

    def select_conflicts_to_resolve():
        mydb = mysql.connector.connect(host='35.246.207.244',
                                       user='root',
                                       password='d0NK3yK0ng',
                                       db='Chatbot')
        cur = mydb.cursor()

        cur.execute("SELECT * FROM requirements_in_conflict WHERE status='original\r'")
        conflicts = cur.fetchall()
        mydb.close()
        return conflicts


class HandleDatabase:
    ids_of_conflicting_requirements = []
    conflicting_requirements_and_ids = []
    conflict_detected = False
    mydb = mysql.connector.connect(host='35.246.207.244',
                                   user='root',
                                   password='d0NK3yK0ng',
                                   db='Chatbot')

    def get_category_description(category):
        print(category)
        description_text = "There is no description"
        mydb = mysql.connector.connect(host='35.246.207.244',
                                       user='root',
                                       password='d0NK3yK0ng',
                                       db='Chatbot')
        cur = mydb.cursor()

        cur.execute('SELECT description,description_name FROM categories WHERE name = %s', (category,))
        description = cur.fetchall()
        if description:
            #description_text = description[0][1] + ". The category is described as: " + description[0][0]
            description_text = "{0}. The category is described as: {1}".format(description[0][1], description[0][0])
        mydb.close()
        return description_text
 
    def get_conflicting_categories(categories):
        conflicts = []
        conflicts.clear()
        mydb = mysql.connector.connect(host='35.246.207.244',
                                       user='root',
                                       password='d0NK3yK0ng',
                                       db='Chatbot')
        cur = mydb.cursor()

        cur.execute('SELECT categories_in_conflict FROM categories WHERE name = %s', (categories,))
        conflicts = cur.fetchall()
        
        if conflicts and conflicts[0][0].find(";"):
            conflicts = conflicts[0][0].split(';')

        mydb.close()
        return conflicts

    def get_conflicting_requirements(all_conflicting_categories):
        if HandleDatabase.conflicting_requirements_and_ids is not None:
            HandleDatabase.conflicting_requirements_and_ids.clear()
        #conn = sqlite3.connect('./database/PrototypeDB.db')
        mydb = mysql.connector.connect(host='35.246.207.244',
                                       user='root',
                                       password='d0NK3yK0ng',
                                       db='Chatbot')
        cur = mydb.cursor()
        
        print("All conflicting categories is 508: ")
        print(all_conflicting_categories)
        if all_conflicting_categories and all_conflicting_categories[0] != "no conflict":
            all_conflicting_categories = all_conflicting_categories[0].split(';')
            for conflict in all_conflicting_categories:
                conflict = '%' + conflict + '%'
                cur.execute("SELECT * FROM requirements WHERE category_original LIKE %s AND status='original'", (conflict,))
                conflicting_requirements_and_ids = cur.fetchall()
                HandleDatabase.conflicting_requirements_and_ids = conflicting_requirements_and_ids
                HandleDatabase.conflict_detected = True
            #if HandleDatabase.conflicting_requirements_and_ids is not None:
            #    HandleDatabase.conflict_detected = True
        else:
            HandleDatabase.conflicting_requirements_and_ids = None
            HandleDatabase.conflict_detected = False
        mydb.close()
        return HandleDatabase.conflicting_requirements_and_ids

    def insert_new_requirement(requirement, categories_by_chatbot, categories_by_user, where_found):#, part_of_system):
        conflict_id = None
        categories_approval = False
        status = "new"
        mydb = mysql.connector.connect(host='35.246.207.244',
                                       user='root',
                                       password='d0NK3yK0ng',
                                       db='Chatbot')
        if categories_by_user is None:
            categories_by_user = categories_by_chatbot

        cur = mydb.cursor()
        
        cur.execute('''INSERT INTO requirements (requirement,
                                                 category_original,
                                                 status,
                                                 agreed_w_category,
                                                 category_by_chatbot,
                                                 category_by_user_2,
                                                 where_found,
                                                 conflict_id,
                                                 user_id)
                       VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (requirement, categories_by_user, status, categories_approval, categories_by_chatbot, categories_by_user, where_found, conflict_id, ""))
        mydb.commit()
        new_requirement_id = cur.lastrowid
        mydb.close()
    
        return new_requirement_id
