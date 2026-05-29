import os
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
# CORS को पूरी तरह ओपन करना
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """
You are the official AI Assistant of 'Blinkfluence', a Noida-based digital marketing and branding agency.
Your behavior preferences: Professional, Friendly, Sales-Focused, Corporate Communication Style.
Languages supported: English and Hindi.

STRICT RULE: You must ONLY answer questions related to Blinkfluence, its services, FAQs, pricing, and contact details provided below. If a user asks anything outside of this context, politely decline to answer.

Authorized Company Data:
1. Introduction: Digital marketing agency in Noida. Specializes in real estate, travel, cafes, doctors, personal branding, corporate business marketing.
2. FAQs: Services include Social Media Management (starts ₹9,000/month), Meta & Google Ads, Website/App Development, Commercial Shoots, LinkedIn marketing, Lead generation. Online consultation via Zoom/Google Meet.
3. Lead Qualification: Business type? Interested services? Budget? Existing website/socials? Business goal? Timeline?
"""

@app.before_request
def handle_options():
    # हर रिक्वेस्ट से पहले OPTIONS (Pre-flight) को संभालना
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        return response

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json or {}
    user_message = data.get("message", "")
    
    if not user_message:
        res = jsonify({"error": "Message is required"})
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res, 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3
        )
        reply = response.choices.message.content
        res = jsonify({"reply": reply})
    except Exception as e:
        res = jsonify({"error": str(e)})
        
    # रिपॉन्स हेडर्स में ओरिजिन अलाउ करना अनिवार्य है
    res.headers.add("Access-Control-Allow-Origin", "*")
    return res

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
