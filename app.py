import schedule
import time
import requests
import json
import uuid
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()


def weekly_task():
    customers = ["carrefour", "colruyt"]
    createChat()

    for customer in customers:
        askAgentInChat("b4a59ce2-1afc-4793-bd55-ebd2e5bab313", customer)

    # Send an email after the task is completed
    subject = "test subject"
    body = "testing body."
    recipient_email = "liano.caekebeke@sap.com"
    send_email(subject, body, recipient_email)

#b4a59ce2-1afc-4793-bd55-ebd2e5bab313
# ---------- Agent API ----------


def getToken():

  url = "https://agents-y0yj1uar.authentication.eu12.hana.ondemand.com/oauth/token"
  headers = {
      "Content-Type": "application/x-www-form-urlencoded"
  }

  data = {
      "grant_type": "client_credentials",
      "client_id": "sb-dffecf4b-ac7b-486a-bf64-a5891a63985f!b726223|unified-ai-agent!b268611",
      "client_secret": "064dda8b-5fcc-4bee-a785-57e37d2e502a$zqrV5_n7095m4ZEdtISL1WuKIJErm4NtcR9DtVKae2A="
  }

  response = requests.post(url, headers=headers, data=data)
  if response.status_code == 200:
      token_data = response.json()
      access_token = token_data.get("access_token")
      return access_token
  else:
      print(f"Error: {response.status_code} - {response.text}")



def createChat(agent="b4a59ce2-1afc-4793-bd55-ebd2e5bab313",name="New conversation"):

  new_chat = str(uuid.uuid4())

  new_chat_data = {
    "ID": new_chat,
    "name": name,
    "history": [
      {
        "ID": "01234567-89ab-cdef-0123-456789abcdef",
        "trace": [
          {
            "ID": "01234567-89ab-cdef-0123-456789abcdef",
            "index": 0,
            "fromId": "string",
            "toId": "string",
            "type": "start",
            "tokenConsumption": [
              {
                "ID": "01234567-89ab-cdef-0123-456789abcdef",
                "modelName": "OpenAiGpt4o",
                "inputTokens": 0,
                "outputTokens": 0
              }
            ],
            "data": "string"
          }
        ],
        "type": "questionForAgent",
        "sender": "ai",
        "content": "string",
        "outputFormat": "string",
        "outputFormatOptions": "string",
        "rating": 0,
        "inputValues": [
          {
            "ID": "01234567-89ab-cdef-0123-456789abcdef",
            "name": "string",
            "description": "string",
            "type": "string",
            "possibleValues": [
              "string"
            ],
            "suggestions": [
              "string"
            ]
          }
        ],
        "source": "string",
        "canceled": False
      }
    ]
  }

  string = "/"+agent+"/chats"
  PostAgentsAPI(string,new_chat_data)
  return new_chat



def PostAgentsAPI(url_request,data=None):
    tk = getToken()

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer "+tk,
        "Content-Type": "application/json"
    }
    url = "https://unified-ai-agent-srv-unified-agent.c-1228ddd.stage.kyma.ondemand.com/api/v1/Agents"+url_request

    if data:
        response = requests.post(url, headers=headers, data=json.dumps(data)) # Send data with the request
    else:
        response = requests.post(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        #print(f"Error: {response.status_code} - {response.text}")
        return response.status_code


def askAgentInChat(agent,chat,msg):
  new_message_data = {
    "msg": msg,
    "async": False,
    "destination": "AGENT_CALLBACK",
    "outputFormat": "Markdown",
    #"outputFormatOptions": "{\"schema\": \"https://json-schema.org/draft/2020-12/schema\"}",
    #"returnTrace": True
  }
  string = "/"+agent+"/chats("+chat+")/UnifiedAiAgentService.sendMessage"
  answer = PostAgentsAPI(string,new_message_data)

  return answer





def send_email(subject, body, recipient_email):
    sender_email = "sap.scoop.news@gmail.com"
    sender_password = os.getenv("EMAIL_PASSWORD")
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")




# Schedule the task to run every sunday at 8:00 AM
schedule.every().thursday.at("13:45").do(weekly_task)
while True:
    schedule.run_pending()
    time.sleep(1)

