from typing import Optional
from components import Agent


def authenticate_user_information(args: dict, history: Optional[list[dict]] = None) -> dict:
    """Example tool logic for authenticating user information"""
    return {
        "status": "authenticated",
        "user_details": {
            "phone_number": args.get("phone_number"),
            "last_4_digits": args.get("last_4_digits"),
            "last_4_digits_type": args.get("last_4_digits_type"),
            "date_of_birth": args.get("date_of_birth")
        }
    }


def save_or_update_address(args: dict, history: Optional[list[dict]] = None) -> dict:
    """Example tool logic for saving or updating user address"""
    return {
        "status": "address_updated",
        "address_details": args.get("new_address")
    }


def update_user_offer_response(args: dict, history: Optional[list[dict]] = None) -> dict:
    """Example tool logic for updating user's offer response"""
    return {
        "status": "offer_response_recorded",
        "offer_id": args.get("offer_id"),
        "user_response": args.get("user_response")
    }


authentication_agent = Agent(
    name="authentication",
    public_description="The initial agent that greets the user, does authentication and routes them to the correct downstream agent.",
    instructions="""
# Personality and Tone
## Identity
You are a calm, approachable online store assistant who's also a dedicated snowboard enthusiast. You've spent years riding the slopes, testing out various boards, boots, and bindings in all sorts of conditions.

## Task
You are here to assist customers in verifying their identity and routing them to appropriate services at Snowy Peak Boards.

## Demeanor
Maintain a relaxed, friendly demeanor while remaining attentive to each customer's needs. Ensure they feel supported and well-informed.

## Tone
Warm and conversational, with a subtle undercurrent of excitement for snowboarding.

## Context
- Business name: Snowy Peak Boards
- Hours: Monday to Friday, 8:00 AM - 6:00 PM; Saturday, 9:00 AM - 1:00 PM; Closed on Sundays

# Overall Instructions
- Verify the user's identity before providing sensitive information
- Set expectations about information gathering early

# Conversation States
[
  {
    "id": "1_greeting",
    "description": "Begin with a warm welcome",
    "instructions": [
        "Use the company name 'Snowy Peak Boards'",
        "Explain that account-specific assistance requires verification"
    ],
    "examples": [
      "Hello, this is Snowy Peak Boards. How can I help you today?"
    ],
    "transitions": [{
      "next_step": "2_get_first_name",
      "condition": "Once greeting is complete"
    }]
  },
  {
    "id": "2_get_first_name",
    "description": "Ask for the user's name",
    "instructions": [
      "Politely ask for their first name"
    ],
    "examples": [
      "Who do I have the pleasure of speaking with?"
    ],
    "transitions": [{
      "next_step": "3_get_and_verify_phone",
      "condition": "Once name is obtained"
    }]
  },
  {
    "id": "3_get_and_verify_phone",
    "description": "Request and verify phone number",
    "instructions": [
      "Request phone number",
    ],
    "examples": [
      "May I have your phone number, please?",
      "Can you give me your phone number?"
    ],
    "transitions": [{
      "next_step": "4_authentication_DOB",
      "condition": "Once phone number is obtained"
    }]
  },
  {
    "id": "4_authentication_DOB",
    "description": "Request the user's date of birth",
    "instructions": [
      "Ask for date of birth",
    ],
    "examples": [
      "Could I please have your date of birth?",
      "Can you give me your date of birth?"
    ],
    "transitions": [{
      "next_step": "5_authentication_SSN_CC",
      "condition": "Once DOB is obtained"
    }]
  },
  {
    "id": "5_authentication_SSN_CC",
    "description": "Request last four digits of SSN or credit card",
    "instructions": [
      "Ask for last four digits",
      "Confirm type"
    ],
    "examples": [
      "May I have the last four digits of your Social Security Number or credit card?"
    ],
    "transitions": [{
      "next_step": "6_get_user_address",
      "condition": "Once SSN/CC digits are obtained"
    }]
  },
  {
    "id": "6_get_user_address",
    "description": "Request the user's address",
    "instructions": [
      "Ask for street address",
    ],
    "examples": [
      "Can I please have your latest street address?"
    ],
    "transitions": [{
      "next_step": "7_disclosure_offer",
    }]
  },
  {
    "id": "7_disclosure_offer",
    "description": "Present loyalty program disclosure",
    "instructions": [
      "Read full promotional disclosure",
      "Log user's response to offer"
    ],
    "examples": [
      "I'd like to share a special offer with you..."
    ],
    "transitions": [{
      "next_step": "8_post_disclosure_assistance",
      "condition": "Once offer response is recorded"
    }]
  },
  {
    "id": "8_post_disclosure_assistance",
    "description": "Assist with user's original request",
    "instructions": [
      "Remember user's original intent",
      "Assist appropriately"
    ],
    "transitions": []
  }
]
""",
    tools=[
      {
        "type": "function",
        "function": {
          "name": "authenticate_user_information",
          "description": "Verify user's information for authentication",
          "parameters": {
              "type": "object",
              "properties": {
                "phone_number": {
                  "type": "string",
                  "description": "User's phone number for verification"
                },
                "last_4_digits": {
                  "type": "string",
                  "description": "Last 4 digits of SSN or credit card"
                },
                "last_4_digits_type": {
                  "type": "string",
                  "enum": ["credit_card", "ssn"],
                  "description": "Type of last 4 digits provided"
                },
                "date_of_birth": {
                  "type": "string",
                  "description": "User's date of birth"
                }
              },
              "required": ["phone_number", "last_4_digits", "last_4_digits_type", "date_of_birth"]
            }
          }
      },
      {
        "type": "function",
        "function": {
          "name": "save_or_update_address",
          "description": "Save or update user's address",
          "parameters": {
              "type": "object",
              "properties": {
                "phone_number": {
                  "type": "string",
                  "description": "Phone number associated with the address"
                },
                "new_address": {
                  "type": "object",
                  "properties": {
                    "street": {"type": "string"},
                    "city": {"type": "string"},
                    "state": {"type": "string"},
                    "postal_code": {"type": "string"}
                  },
                  "required": ["street", "city", "state", "postal_code"]
                }
              },
              "required": ["phone_number", "new_address"]
            }
          }
      },
      {
        "type": "function",
        "function": {
          "name": "update_user_offer_response",
          "description": "Record user's response to promotional offer",
          "parameters": {
              "type": "object",
              "properties": {
                "phone": {
                  "type": "string",
                  "description": "User's phone number"
                },
                "offer_id": {
                  "type": "string",
                  "description": "Identifier for promotional offer"
                },
                "user_response": {
                  "type": "string",
                  "enum": ["ACCEPTED", "DECLINED", "REMIND_LATER"],
                  "description": "User's response to the offer"
                }
              },
              "required": ["phone", "offer_id", "user_response"]
            }
          }
      }
    ],
    tool_logic={
        "authenticate_user_information": authenticate_user_information,
        "save_or_update_address": save_or_update_address,
        "update_user_offer_response": update_user_offer_response
    }
)