import os
from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


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
        app.logger.info(f"Received message: {user_msg}")
        
        # Generate content using the AI model
        generated_response = genai.GenerativeModel(model_name = "gemini-1.5-pro-latest" ).generate_content(  # Use the correct method from the documentation
           {"parts": [user_msg]}
        )
        app.logger.info(f"Generated response from AI: {generated_response}")

        # Extract the generated text from the response
        if generated_response.candidates:
            generated_text = generated_response.candidates[0].content.parts[0].text.strip()
            app.logger.info(f"Generated text: {generated_text}")

            # Send a reply message using Twilio
            try:
                response.message(generated_text)
            except Exception as twilio_error:
                app.logger.error(f"Twilio error: {twilio_error}")
                response.message("Sorry, there was an issue sending the message.")

        else:
            app.logger.error("No candidates in the generated response")
            response.message("Sorry, I couldn't generate a response at the moment.")

    except Exception as e:
        # Log the exception
        app.logger.error(f"Error processing request: {e}")
        # Handle any errors that occur during generation or sending the message
        response.message("Sorry, I couldn't process your request at the moment.")

    # Return the Twilio response as a string
    return str(response)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
