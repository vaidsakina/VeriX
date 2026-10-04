import os
import google.generativeai as genai


# -----------------------------
# Gemini configuration
# -----------------------------

genai.configure(
    api_key=os.getenv("google_api")
)


generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
}


model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=generation_config
)


# -----------------------------
# Text claim analysis
# -----------------------------

def get_response(userInput, reference_results=None):

    if reference_results is None:
        reference_results = []

    reference_text = ""

    if reference_results:

        reference_text = "\n\nLocal reference database records:\n"

        for row in reference_results:

            reference_text += f"""
Title: {row[1]}
Content: {row[2]}
Verdict stored in database: {row[3]}
Source: {row[4]}
Category: {row[5]}
Date added: {row[6]}
---
"""

    else:

        reference_text = """
No matching record was found in the local reference database.
"""


    prompt = f"""
You are VeriX, an AI-assisted misinformation analysis system.

Analyze the following claim or message.

Your task is NOT to blindly call everything true or false.

Use these four assessment categories:

1. Likely reliable
2. Potentially misleading
3. Potential misinformation
4. Cannot be verified from the provided information

Give your answer in this format:

Assessment:
[one of the four categories]

Explanation:
[short and clear explanation]

Database Reference:
[If a relevant local database record exists, explain briefly how
it relates to the claim. If there is no relevant record, say:
"No matching reference found in the local database."]

What to verify:
[what the user should check before believing or sharing the claim]

Important:
- The local database is a reference knowledge base, not an absolute
  source of truth.
- Do not treat a database record as proof by itself.
- Do not invent sources or facts.
- If the available information is insufficient, say that it cannot
  be verified.
- Do not claim certainty when the evidence is insufficient.

Claim:
{userInput}

{reference_text}
"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        print("Text analysis error:", e)

        return "Unable to analyze the claim at this time."


# -----------------------------
# Image analysis
# -----------------------------

def analyze_image(image_path, mime_type=None):

    try:

        with open(image_path, "rb") as f:
            image_data = f.read()

        if not mime_type:
            mime_type = "image/jpeg"

        prompt = """
You are VeriX, an AI-assisted misinformation analysis system.

Analyze this image for possible misinformation, manipulation,
misleading context, fake claims, or edited content.

Do not automatically declare the image fake simply because it
looks unusual.

Give the result in this format:

Assessment:
[Likely reliable / Potentially misleading /
Potential misinformation / Cannot be verified]

Explanation:
[short explanation]

What to verify:
[what should be checked before trusting or sharing this image]

If the image contains text, consider that text as part of the analysis.

Important:
AI analysis does not guarantee that an image is genuine or fake.
Do not invent facts or sources.
"""

        response = model.generate_content([
            {
                "role": "user",
                "parts": [
                    {
                        "mime_type": mime_type,
                        "data": image_data
                    },
                    {
                        "text": prompt
                    }
                ]
            }
        ])

        return response.text

    except Exception as e:

        print("Image analysis error:", e)

        return "Unable to analyze the image."


# -----------------------------
# Audio analysis
# -----------------------------

def analyze_audio(audio_path, mime_type=None):

    try:

        with open(audio_path, "rb") as f:
            audio_data = f.read()

        if not mime_type:
            mime_type = "audio/mpeg"

        prompt = """
You are VeriX, an AI-assisted misinformation analysis system.

Analyze this audio for claims that may be false, misleading,
out of context, manipulated, or presented without sufficient evidence.

Give the result in this format:

Assessment:
[Likely reliable / Potentially misleading /
Potential misinformation / Cannot be verified]

Explanation:
[short explanation]

What to verify:
[what should be checked before trusting or sharing this audio]

Do not claim something is false merely because there is insufficient
information to verify it.

AI analysis does not guarantee that the audio is true or false.
"""

        response = model.generate_content([
            {
                "role": "user",
                "parts": [
                    {
                        "mime_type": mime_type,
                        "data": audio_data
                    },
                    {
                        "text": prompt
                    }
                ]
            }
        ])

        return response.text

    except Exception as e:

        print("Audio analysis error:", e)

        return "Unable to analyze the audio."


# -----------------------------
# Video analysis
# -----------------------------

def analyze_video(video_path, mime_type=None):

    try:

        with open(video_path, "rb") as f:
            video_data = f.read()

        if not mime_type:
            mime_type = "video/mp4"

        prompt = """
You are VeriX, an AI-assisted misinformation analysis system.

Analyze this video for possible misinformation, manipulated content,
misleading claims, fake context, or misleading presentation.

Give the result in this format:

Assessment:
[Likely reliable / Potentially misleading /
Potential misinformation / Cannot be verified]

Explanation:
[short explanation]

What to verify:
[what should be checked before trusting or sharing this video]

Pay attention to:
- visible text
- spoken claims
- visual content
- context presented in the video

Do not automatically classify a video as misinformation just because
it cannot be completely verified.

AI analysis does not guarantee that the video is true or false.
"""

        response = model.generate_content([
            {
                "role": "user",
                "parts": [
                    {
                        "mime_type": mime_type,
                        "data": video_data
                    },
                    {
                        "text": prompt
                    }
                ]
            }
        ])

        return response.text

    except Exception as e:

        print("Video analysis error:", e)

        return "Unable to analyze the video."
