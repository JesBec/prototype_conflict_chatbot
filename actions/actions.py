from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import (SlotSet, EventType)
#from rasa_core.channels.slack import SlackInput

import requests
import random
import sqlite3
from sqlite3 import Error

class ValidateCategoryForm(FormValidationAction):

    slots_to_reset = ["new_requirement",
    "intent_new_requirement",
    "conflicting_requirements",
    "agreement_on_categorization",
    "categorization_requirement_user",
    "more_information_categories_needed",
    "does_participate",
    "agrees_with_conflict",
    "explanation_conflict",
    "preference",
    "explanation_preference",
    "when_discovered",
    "does_participate_user",
    "age",
    "main_use",
    "user_group",
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
 
    def name(self) -> Text:
        return "validate_category_form"

    async def required_slots(self, slots_mapped_in_domain: List[Text], dispatcher: "CollectingDispatcher",tracker: "Tracker", domain: "DomainDict",
    ) -> Optional[List[Text]]:
        agreement = tracker.slots.get("agreement_on_categorization")
        #dispatcher.utter_message("agreement on categorization")
        #dispatcher.utter_message(tracker.slots.get("categorization_requirement_user"))
        if tracker.slots.get("categorization_requirement_user"):
            category = tracker.slots.get("categorization_requirement_user")
            new_slot = "sub_category_" + category
            if new_slot != "sub_category_nocategory" and new_slot != "sub_category_changereq":
                additional_slots = ["categorization_requirement_user"]
                additional_slots.append(new_slot)
                return additional_slots + slots_mapped_in_domain
            #return slots_mapped_in_domain

        if agreement == "/deny":
            additional_slots = ["agreement_on_categorization"]
            additional_slots.append("categorization_requirement_user")
            return additional_slots + slots_mapped_in_domain

        elif agreement == "/more_information_about_categories":
            additional_slots = ["agreement_on_categorization"]
            additional_slots.append("more_information_categories_needed")
            return additional_slots + slots_mapped_in_domain

        return slots_mapped_in_domain
        

    async def extract_agreement_on_categorization(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        agreement = ""
        if tracker.get_slot("agreement_on_categorization"):
            return {"agreement_on_categorization": tracker.get_slot("agreement_on_categorization")}
        elif tracker.get_intent_of_latest_message() == "affirm":
            agreement = tracker.get_intent_of_latest_message()
        elif tracker.get_intent_of_latest_message() == "deny":
            agreement = tracker.get_intent_of_latest_message()
        elif tracker.get_intent_of_latest_message() == "more_information_about_categories":
            agreement = tracker.get_intent_of_latest_message()
        else:
            agreement = tracker.get_slot("agreement_on_categorization") 

        return {"agreement_on_categorization": agreement}

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
            return {"agreement_on_categorization" : None, "more_information_categories_needed" : False}
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
            # if tracker.get_slot("sub_category_livetranscript") == "goback":
            #     return {"sub_category_livetranscript" : None, "categorization_requirement_user" : None}
            return {"sub_category_livetranscript" : tracker.get_slot("sub_category_livetranscript")}
        return {"sub_category_livetranscript" : tracker.get_intent_of_latest_message()}

    async def extract_sub_category_polling(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        if tracker.get_slot("sub_category_polling"):
            # if tracker.get_slot("sub_category_polling") == "goback":
            #     dispatcher.utter_message("In go back if")
            #     return {"sub_category_polling" : None, "categorization_requirement_user" : None}
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
        if tracker.get_slot("requested_slot") == "new_requirement":

            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. No requirement was submitted. Let me know when you have a new requirement.")
                return {"requested_slot" : None}
            if tracker.get_intent_of_latest_message() == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"new_requirement" : None}
            if tracker.get_intent_of_latest_message() == "explain":
                dispatcher.utter_message("Requirements explain the behaviour you want from our system. We need this information to see what you expect from our system. We will check if your requirement is in conflict with other requirements to see if we can implement it. If you would like to, I can tell you more about how to formulate a requirement.")
                return {"new_requirement" : None}
            if tracker.get_intent_of_latest_message() == "explain_how_to_requirement":
                dispatcher.utter_message("Here is an example of a requirement:\"The camera should be turned on when the meeting is started.\". Just try to be as precise as possible.")
                return {"new_requirement" : None}
        return {"intent_new_requirement" : tracker.get_intent_of_latest_message(), "categorization_info" : HandleDatabase.get_category_description(tracker.get_intent_of_latest_message())}

    def validate_agreement_on_categorization(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        if tracker.get_slot("requested_slot") == "agreement_on_categorization":
            if tracker.get_slot("agreement_on_categorization") == "/changereq":
                dispatcher.utter_message("Of course. You can change it now.")
                return {"agreement_on_categorization" : None, "new_requirement" : None}
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. No requirement was submitted. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
        return {"agreement_on_categorization" : tracker.get_slot("agreement_on_categorization")}
    
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
                return {"agreement_on_categorization" : None}
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
                return {"categorization_requirement_user" : None, "agreement_on_categorization" : None, "new_requirement" : None}
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

        #if tracker.get_slot("does_participate"):
        #    dispatcher.utter_message("does_participate")
        #    dispatcher.utter_message(tracker.get_slot("does_participate"))
        #if tracker.get_slot("agrees_with_conflict"):
        #    dispatcher.utter_message("agrees_with_conflict")
            #dispatcher.utter_message(tracker.get_slot("agrees_with_conflict"))
        #agrees_w_confl = tracker.get_slot("agrees_with_conflict")
        #dispatcher.utter_message("agrees with conflict:")
        #dispatcher.utter_message(agrees_w_confl)
        if tracker.get_slot("does_participate") == True:
            additional_slots = ["does_participate"]
            #additional_slots.append("agrees_with_conflict")
            if tracker.get_slot("agrees_with_conflict"):
                #dispatcher.utter_message(tracker.get_slot("agrees_with_conflict"))
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

    # async def extract_agrees_with_conflict(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    # ) -> Dict[Text, Any]:
    #     agrees = None
    #     dispatcher.utter_message(tracker.get_intent_of_latest_message())
    #     if tracker.get_slot("agrees_with_conflict"):
    #         agrees = tracker.get_slot("agrees_with_conflict")
    #     if tracker.get_intent_of_latest_message() == "affirm":
    #         agrees = True
    #     elif tracker.get_intent_of_latest_message() == "deny":
    #         agrees = False
    #     #agrees = None
    #     #if tracker.get_slot("agrees_with_conflict"):
    #     #    agrees = tracker.get_slot("agrees_with_conflict")
    #     #dispatcher.utter_message("in extract agrees with conflict")
    #     #dispatcher.utter_message(tracker.get_intent_of_latest_message())
    #     return {"agrees_with_conflict" : agrees}

    async def extract_explanation_conflict(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        return {"explanation_conflict" : tracker.latest_message.get("text")}

    async def extract_preference(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
       # message = tracker.latest_message.get("text") #no_answer
        preference = None
        if tracker.get_slot("preference"):
            preference = tracker.get_slot("preference")
        #preference = None
        #if tracker.get_slot("requested_slot") == "preference":
        #    if tracker.get_slot("preference"):
        #        preference = tracker.get_slot("preference")
        #    if tracker.get_intent_of_latest_message() == "no_answer":
        #       dispatcher.utter_message(text="Allright. It is fine if you do not want to answer this question. We will skip it then.")
        #       return {"preference" : "null", "explanation_preference" : "null"}
        #    if "first" in message:
        #        preference = "first"
        #    elif "last" in message:
        #        preference = "last"
        return {"preference" : preference}

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
        #dispatcher.utter_message(tracker.get)
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
        return {"does_participate" : does_participate, "agrees_with_conflict" : slot_value}

    def validate_agrees_with_conflict(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        dispatcher.utter_message(tracker.get_slot("agrees_with_conflict"))
        if tracker.get_slot("requested_slot") == "agrees_with_conflict":
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"agrees_with_conflict" : None}
            if tracker.get_intent_of_latest_message() == "explain": 
                dispatcher.utter_message("We need your help to see if this is a real conflict. A conflict exists when two requirements cannot be implemented in the same system. E.g., they could contradict each other like \"camera on by default\" or \"camera off by default\". Sometimes constraints can hinder the implementation of requirements such as \"only the host can turn off the microphone of all participants\".")
                return {"agrees_with_conflict" : None}
            if tracker.get_intent_of_latest_message() == "no_idea": 
                dispatcher.utter_message("No problem. Should I explain to you why we ask this questions and what a conflict is? You can also skip this question if you tell me to.")
                return {"agrees_with_conflict" : None}
            if tracker.get_intent_of_latest_message() == "no_answer": 
                dispatcher.utter_message(text="Allright. It is fine if you do not want to answer this question. We will skip it then.")
                return {"agrees_with_conflict" : "no answer", "explanation_conflict" : "no answer"}
            if tracker.get_intent_of_latest_message() == "affirm":
                return {"agrees_with_conflict" : True}
            elif tracker.get_intent_of_latest_message() == "deny":
                #dispatcher.utter_message("in false agrees with")
                return {"agrees_with_conflict" : False}
        return {"agrees_with_conflict" : tracker.get_slot("agrees_with_conflict")}

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
            #additional_slots.append("agrees_with_conflict")
            if tracker.get_slot("agrees_with_conflict"):
                #dispatcher.utter_message(tracker.get_slot("agrees_with_conflict"))
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
            elif intent == "affirm":
                does_participate = True
        return {"does_participate" : does_participate}

    # async def extract_agrees_with_conflict(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    # ) -> Dict[Text, Any]:
    #     #agrees = None
    #     #if tracker.get_slot("agrees_with_conflict"):
    #     #    agrees = tracker.get_slot("agrees_with_conflict")
    #     #elif tracker.get_intent_of_latest_message() == "affirm":
    #     #    agrees = True
    #     #elif tracker.get_intent_of_latest_message() == "deny":
    #     #    agrees = False
    #     #_message("in extract agrees with conflict")
    #     #dispatcher.utter_message(tracker.get_intent_of_latest_message())
    #     return {"agrees_with_conflict" : tracker.get_intent_of_latest_message()}

    async def extract_explanation_conflict(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        return {"explanation_conflict" : tracker.latest_message.get("text")}

    async def extract_preference(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
       # message = tracker.latest_message.get("text") #no_answer
        preference = None
        if tracker.get_slot("preference"):
            preference = tracker.get_slot("preference")
        #preference = None
        #if tracker.get_slot("requested_slot") == "preference":
        #    if tracker.get_slot("preference"):
        #        preference = tracker.get_slot("preference")
        #    if tracker.get_intent_of_latest_message() == "no_answer":
        #       dispatcher.utter_message(text="Allright. It is fine if you do not want to answer this question. We will skip it then.")
        #       return {"preference" : "null", "explanation_preference" : "null"}
        #    if "first" in message:
        #        preference = "first"
        #    elif "last" in message:
        #        preference = "last"
        return {"preference" : preference}

    async def extract_explanation_preference(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        return {"explanation_preference" : tracker.latest_message.get("text")}

    async def extract_when_discovered(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        return {"when_discovered" : tracker.latest_message.get("text")}

    def validate_agrees_with_conflict(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        dispatcher.utter_message(tracker.get_slot("agrees_with_conflict"))
        if tracker.get_slot("requested_slot") == "agrees_with_conflict":
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"agrees_with_conflict" : None}
            if tracker.get_intent_of_latest_message() == "explain":
                dispatcher.utter_message("We need your help to see if this is a real conflict. A conflict exists when two requirements cannot be implemented in the same system. E.g., they could contradict each other like \"camera on by default\" or \"camera off by default\". Sometimes constraints can hinder the implementation of requirements such as \"only the host can turn off the microphone of all participants\".")
                return {"agrees_with_conflict" : None}
            if tracker.get_intent_of_latest_message() == "no_idea":
                dispatcher.utter_message("No problem. Should I explain to you why we ask this questions and what a conflict is? You can also skip this question if you tell me to.")
                return {"agrees_with_conflict" : None}
            if tracker.get_intent_of_latest_message() == "no_answer":
                dispatcher.utter_message(text="Allright. It is fine if you do not want to answer this question. We will skip it then.")
                return {"agrees_with_conflict" : "no answer", "explanation_conflict" : "no answer"}
            if tracker.get_intent_of_latest_message() == "affirm":
               return {"agrees_with_conflict" : True}
            elif tracker.get_intent_of_latest_message() == "deny":
            #dispatcher.utter_message("in false agrees with")
               return {"agrees_with_conflict" : False}
        return {"agrees_with_conflict" : tracker.get_slot("agrees_with_conflict")}

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
        return {"age" : slot_value, "main_use" : slot_value, "user_group" : slot_value, "does_participate_user" : agrees}

    def validate_age(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if tracker.get_slot("requested_slot") == "age":
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"age" : None}
            if tracker.get_intent_of_latest_message() == "explain":
                dispatcher.utter_message("We are only asking this to see if different user groups have different needs. You can choose to skip this question.")
                return {"age" : None}
            if tracker.get_intent_of_latest_message() == "no_answer":
                dispatcher.utter_message("You do not have to answer. We will skip this question.")
                return {"age" : "no answer"}
            if tracker.get_intent_of_latest_message() == "no_idea": 
                dispatcher.utter_message("Should I explain to you why we ask this question? You can also skip this question if you tell me to.")
                return {"age" : None}
        return {"age" : slot_value}

    def validate_main_use(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if tracker.get_slot("requested_slot") == "main_use":
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"main_use" : None}
            if tracker.get_intent_of_latest_message() == "explain":
                dispatcher.utter_message("If we know in which contexts the system gets used, we can work on adding features that will improve your experience.")
                return {"main_use" : None}
            if tracker.get_intent_of_latest_message() == "no_answer":
                dispatcher.utter_message("You do not have to answer. We will skip this question.")
                return {"main_use" : "no answer"}
            if tracker.get_intent_of_latest_message() == "no_idea": 
                dispatcher.utter_message("Should I explain to you why we ask this question? You can also skip this question if you tell me to.")
                return {"main_use" : None}
        return {"main_use" : slot_value}

    def validate_user_group(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        if tracker.get_slot("requested_slot") == "user_group":
            if tracker.get_intent_of_latest_message() == "stop":
                dispatcher.utter_message("Allright. We will stop asking questions. Let me know when you have a new requirement.")
                return {slot : None for slot in ValidateCategoryForm.slots_to_reset}
            if tracker.get_intent_of_latest_message() == "chitchat":
                dispatcher.utter_message(text=f"This is not the purpose I am intented for. I can help you submit new features and you can help me to resolve conflicts if you would like to.")
                return {"user_group" : None}
            if tracker.get_intent_of_latest_message() == "explain":
                dispatcher.utter_message("Knowing to which user group you belong will tell us to focus on features catering to the needs of this user group.")
                return {"user_group" : None}
            if tracker.get_intent_of_latest_message() == "no_answer":
                dispatcher.utter_message("You do not have to answer. We will skip this question.")
                return {"user_group" : "no answer"}
            if tracker.get_intent_of_latest_message() == "no_idea": 
                dispatcher.utter_message("Should I explain to you why we ask this question? You can also skip this question if you tell me to.")
                return {"user_group" : None}
        return {"user_group" : slot_value}


class ActionDatabase(Action):
    categories_requirement = None
    round = 0
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

        if ActionDatabase.round == 0:
            message_for_user = ""
        
            if tracker.get_slot("agreement_on_categorization") == "/affirm":
                ActionDatabase.categories_requirement = tracker.get_slot("intent_new_requirement")
         
            elif tracker.get_slot("agreement_on_categorization") == "/deny":
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
        
            ActionDatabase.round = 1
            return [SlotSet("conflicting_requirements", message_conflict)]
        return


class ActionSaveInformation(Action):
    user_id = None
    def name(self) -> Text:
         return "action_save_information"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #if tracker.get_slot("new_requirement") and tracker.get_slot("intent_new_requirement"):

            #category_new_requirement = tracker.get_slot("intent_new_requirement")
            #if ActionDatabase.categories_requirement is not None:
            #    category_new_requirement = ActionDatabase.categories_requirement

            #new_requirement_id = HandleDatabase.insert_new_requirement(tracker.get_slot("new_requirement"), 
            #                                          category_new_requirement, 
            #                                          ActionDatabase.categories_requirement, 
            #                                          tracker.get_slot("when_discovered"))

            #if HandleDatabase.conflict_detected == True:
            #    HandleConflictManagement.conflict_1_id = new_requirement_id
        
            ##elif HandleConflictManagement.conflict_db_id is not None:
            ##    HandleConflictManagement.update_conflict(tracker.get_slot("preference"),HandleConflictManagement.conflict_db_id)

            #else:
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
                                                    votes_requirement_1,
                                                    votes_requirement_2,
                                                    tracker.get_slot("explanation_preference"))

        if tracker.get_slot("does_participate_user") == True and ActionSaveInformation.user_id is None:
            ActionSaveInformation.user_id = HandleConflictManagement.insert_user_information(tracker.get_slot("age"), 
                                                                    tracker.get_slot("main_use"), 
                                                                    tracker.get_slot("user_group"))
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
                        "agrees_with_conflict",
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
                elif  tracker.get_slot("preference") == "last":
                    votes_requirement_2 = 1

                ActionSaveFirstConflict.conflict_id = HandleConflictManagement.insert_conflict(HandleConflictManagement.conflict_1_id, #needs to be saved if conflicts from DB
                                                         HandleConflictManagement.conflict_2_id,#requirement_2_id, #needs
                                                         tracker.get_slot("agrees_with_conflict"), 
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
                message_conflict = "\" " + selected_conflict[0][1] + "\" (" + selected_conflict[0][2] + ") and \"" + selected_conflict[1][1] + "\" (" + selected_conflict[1][2] +")"
            else:
                message_conflict = "No conflict found."

            return [SlotSet("does_participate", None),
                    SlotSet("agrees_with_conflict", None),
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

    def select_conflict(category_new_requirement, new_requirement):
        text = None
        conflicts = []
        conflict_information_found = False
        print("Conflict detected")
        print(HandleDatabase.conflict_detected)
        print("Saved conflicts in array")
        print(conflicts)
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
                HandleConflictManagement.conflict_2_id = chosen_conflict[0]
                chosen_conflict_2 = [chosen_conflict[0], chosen_conflict[1], chosen_conflict[2]]
        
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
               print("HandleConflictManagement.conflicts_from_db")
               print(HandleConflictManagement.conflicts_from_db)
               print("chosen_conflict")
               print(chosen_conflict)
               HandleConflictManagement.conflict_db_id = chosen_conflict[0]

               conn = sqlite3.connect('./database/PrototypeDB.db')
               cur = conn.cursor()
               cur.execute('''SELECT rowid,* FROM requirements WHERE rowid = ? OR rowid = ?''', (chosen_conflict[1],chosen_conflict[2]))
               selected_conflicts_db = cur.fetchall()
               print("requirements from conflicts")
               print(selected_conflicts_db)

               if selected_conflicts_db and selected_conflicts_db is not None:
                   conflict_1 = [selected_conflicts_db[0][0],selected_conflicts_db[0][1],selected_conflicts_db[0][2]]
                   conflict_2 = [selected_conflicts_db[1][0],selected_conflicts_db[1][1],selected_conflicts_db[1][2]]
                   conflicts.append(conflict_1)
                   conflicts.append(conflict_2)
                   HandleConflictManagement.conflict_1_id = conflicts[0][0]
                   HandleConflictManagement.conflict_2_id = conflicts[1][0]
               
        print("Those are the chosen conflicts:")
        print(conflicts)
        return conflicts
        

    def insert_conflict(requirement_1_id, requirement_2_id, user_agreed_conflict, reasoning_conflict, 
                        votes_requirement_1,votes_requirement_2,reasoning_preference):
        conn = sqlite3.connect('./database/PrototypeDB.db')
        cur = conn.cursor()

        cur.execute('INSERT INTO requirements_in_conflict VALUES (?,?,?,?,?,?,?,?)', (requirement_1_id,
                                                                                      requirement_2_id,
                                                                                      user_agreed_conflict,
                                                                                      reasoning_conflict,
                                                                                      votes_requirement_1, 
                                                                                      votes_requirement_2,
                                                                                      reasoning_preference,
                                                                                      "new"))
        conn.commit()
        conflict_id = cur.lastrowid
        
        return conflict_id
    
    def update_conflict(preference,rowid):
        conn = sqlite3.connect('./database/PrototypeDB.db')
        cur = conn.cursor()

        if preference == "first":
            cur.execute('UPDATE requirements_in_conflict SET votes_requirment_1 = 1, votes_requirement_2 = 0 WHERE rowid = ?', (rowid,))
            conn.commit()
        elif preference == "last":
            cur.execute('UPDATE requirements_in_conflict SET votes_requirement_1 = 0, votes_requirement_2 = 1 WHERE rowid = ?', (rowid,))
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

    def select_conflicts_to_resolve():
        conn = sqlite3.connect('./database/PrototypeDB.db')
        cur = conn.cursor()

        cur.execute("SELECT rowid,* FROM requirements_in_conflict WHERE status='original'")
        return cur.fetchall()


class HandleDatabase:
    ids_of_conflicting_requirements = []
    conflicting_requirements_and_ids = []
    conflict_detected = False

    def get_category_description(category):
        conn = sqlite3.connect('./database/PrototypeDB.db')
        cur = conn.cursor()

        cur.execute('SELECT description,description_name FROM categories WHERE name = ?', (category,))
        description = cur.fetchall()

        description_text = description[0][1] + " The category is described as: " + description[0][0]
        return description_text

    
    def get_conflicting_categories(categories):
        conflicts = []
        conflicts.clear()
        conn = sqlite3.connect('./database/PrototypeDB.db')
        cur = conn.cursor()

        cur.execute('SELECT categories_in_conflict FROM categories WHERE name = ?', (categories,))
        conflicts = cur.fetchall()
        
        if conflicts and conflicts[0][0].find(";"):
            conflicts = conflicts[0][0].split(';')
        
        conn.close()
        return conflicts

    def get_conflicting_requirements(all_conflicting_categories):
        if HandleDatabase.conflicting_requirements_and_ids is not None:
            HandleDatabase.conflicting_requirements_and_ids.clear()
        conn = sqlite3.connect('./database/PrototypeDB.db')
        cur = conn.cursor()
        
        print("All conflicting categories is 508: ")
        print(all_conflicting_categories)
        if all_conflicting_categories and all_conflicting_categories[0] != "no conflict":
            all_conflicting_categories = all_conflicting_categories[0].split(';')
            for conflict in all_conflicting_categories:
                conflict = '%' + conflict + '%'
                cur.execute('SELECT rowid,* FROM requirements WHERE category_original LIKE ?', (conflict,))
                conflicting_requirements_and_ids = cur.fetchall()
                HandleDatabase.conflicting_requirements_and_ids = conflicting_requirements_and_ids
                HandleDatabase.conflict_detected = True
        else:
            HandleDatabase.conflicting_requirements_and_ids = None
            HandleDatabase.conflict_detected = False


        conn.close()
        return HandleDatabase.conflicting_requirements_and_ids


    def insert_new_requirement(requirement, categories_by_chatbot, categories_by_user, where_found):#, part_of_system):
        conflict_id = None
        categories_approval = False
        status = "new"
        if categories_by_user is None:
            categories_by_user = categories_by_chatbot
        conn = sqlite3.connect('./database/PrototypeDB.db')
        cur = conn.cursor()
        
        cur.execute('INSERT INTO requirements VALUES(?,?,?,?,?,?,?,?,?)', (requirement, categories_by_user, status, categories_approval, categories_by_chatbot, categories_by_user, where_found, conflict_id, ""))
        conn.commit()
        new_requirement_id = cur.lastrowid
        conn.close()
    
        return new_requirement_id

    # old way to put all conflicts into the table, that have not been evaluated by user
    def insert_conflicts_table(requirements_and_ids, new_requirement, new_requirement_id, reasoning, votes_requirement_1, votes_requirement_2):#,part_of_system):
        
        conn = sqlite3.connect('./database/PrototypeDB.db')
        cur = conn.cursor()

        new_conflicts = []
        for requirement_and_id in requirements_and_ids:
                    new_conflicts.append([new_requirement_id, requirement_and_id[0], reasoning, votes_requirement_1, votes_requirement_2])
                    
        cur.executemany('INSERT INTO requirements_in_conflict VALUES (?,?,?,?,?,?,?)', (new_conflicts))
        conn.commit()
    