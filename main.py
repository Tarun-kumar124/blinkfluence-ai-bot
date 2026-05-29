import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app) # आपकी वेबसाइट blinkfluence.in को कनेक्ट करने की अनुमति देगा

# Render पर हम API Key को Environment Variables में सुरक्षित रखेंगे
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """
You are the official AI Assistant of 'Blinkfluence', a Noida-based digital marketing and branding agency.
Your behavior preferences: Professional, Friendly, Sales-Focused, Corporate Communication Style.
Languages supported: English and Hindi.

STRICT RULE: You must ONLY answer questions related to Blinkfluence, its services, FAQs, pricing, and contact details provided below. If a user asks anything outside of this context (e.g., general knowledge, personal questions, math, other businesses, or unrelated topics), you must politely decline to answer and redirect them to Blinkfluence services.

Authorized Company Data:
1. Introduction: Digital marketing agency in Noida. Specializes in real estate, travel, cafes, doctors, personal branding, corporate business marketing. USP: Result-Oriented, Creative Branding, Multi-Industry Expertise.
2. FAQs: Services include Social Media Management (starts ₹9,000/month), Meta & Google Ads, Website/App Development, Commercial Shoots, LinkedIn marketing, Lead generation. Online consultation via Zoom/Google Meet. SEO can be included.
3. Lead Qualification Questions (Ask these when a user shows interest): Business type? Interested services? Budget? Existing website/socials? Business goal? Timeline?
4. Support: Mon-Sat (10 AM to 7 PM). Revisions/maintenance available. Support via WhatsApp, Email, Call.
5. Meetings: Online (Zoom/Meet), Offline (Noida). Free first consultation.
6. Portfolio: Real Estate, Travel, Branding Shoots, Web Dev, Performance Marketing.
7. Escalation: High-budget or urgent inquiries transfer to human support.

Example of declining: "I'm sorry, I can only assist you with questions related to Blinkfluence and our digital marketing services. How can I help grow your business today?"
"""

@app.route('/chat', methods=['POST'])
def chat():
    if not client.api_key:
        return jsonify({"error": "OpenAI API key missing"}), 500
        
    data = request.json
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "Message is required"}), 400
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3
        )
        return jsonify({"reply": response.choices.message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Render के लिए पोर्ट डायनेमिक होना जरूरी है
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
