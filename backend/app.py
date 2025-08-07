# backend/app.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# The new V3 client
from google.cloud import translate
from dotenv import load_dotenv

# This line loads the .env file
load_dotenv()

app = Flask(__name__)
# This allows your frontend (on a different port) to communicate with this backend
CORS(app)

# V3 API requires your Project ID and a location.
project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
location = "global"  # Use "global" for non-regionalized models
parent = f"projects/{project_id}/locations/{location}"

# Initialize the V3 client
translate_client = translate.TranslationServiceClient()


@app.route("/translate", methods=["POST"])
def translate_text():
    # Get the data from the frontend's request
    data = request.get_json()
    if not data or "text" not in data or "target_lang" not in data:
        return jsonify({"error": "Invalid request body"}), 400

    text_to_translate = data["text"]
    target_language = data["target_lang"]

    try:
        # Construct the V3 API request
        response = translate_client.translate_text(
            parent=parent,
            contents=[text_to_translate],
            mime_type="text/plain",
            source_language_code="en",
            target_language_code=target_language,
        )

        # Parse the V3 response
        translated_text = response.translations[0].translated_text
        return jsonify({"translated_text": translated_text})

    except Exception as e:
        print(f"An error occurred with the Translation API: {e}")
        return jsonify({"error": "Translation failed"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
