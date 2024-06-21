import os
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Configure the Generative AI API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Flask app
app = Flask(__name__)

@app.route("/", methods=["POST"])
def bot():
    # User input from Twilio's POST request
    user_msg = request.values.get('Body', '').lower()

    # Create a Twilio response object
    response = MessagingResponse()

    try:
        # Generate content using the AI model
        generated_response = genai.generate_content(
            model_name="gemini-1.5-pro-latest",
            prompt={"role": "user", "parts": [user_msg]}
        )

        # Extract the generated text from the response
        generated_text = generated_response.candidates[0].content.parts[0].text.strip()

        # Send a reply message using Twilio
        client.messages.create(
            body=generated_text,
            from_='+14155238886',
            to='+201507772562'
        )

        # Create a message with the generated text in response
        msg = response.message(f"Generated response: {generated_text}")

    except Exception as e:
        # Handle any errors that occur during generation or sending the message
        msg = response.message("Sorry, I couldn't process your request at the moment.")

    # Return the Twilio response as a string
    return str(response)

if __name__ == "__main__":
    app.run()
