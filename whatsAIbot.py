import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Generative AI API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name= "gemini-1.5-pro-latest")

# Initialize the Flask app
app = Flask(__name__)

@app.route("/", methods=["POST"])
def bot():
    # User input from Twilio's POST request
    user_msg = request.values.get('Body', '').lower()

    # Create a Twilio response object
    response = MessagingResponse()

    try:
        # Generate content using the AI model
        generated_response = model.generate_content(
            {"role": "user", "parts": [user_msg]}
        )

        # Extract the generated text from the response
        generated_text = generated_response.candidates[0].content.parts[0].text.strip()

        # Create a message with the generated text
        msg = response.message(generated_text)

    except Exception as e:
        # Handle any errors that occur during generation
        msg = response.message("Sorry, I couldn't process your request at the moment.")

    # Return the Twilio response as a string
    return str(response)

if __name__ == "__main__":
    app.run()
