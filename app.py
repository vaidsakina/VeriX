from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename

from chat import (
    get_response,
    analyze_image,
    analyze_audio,
    analyze_video
)

from database import create_db, search_misinformation

import os


app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)

CORS(app)


# -----------------------------
# Database initialization
# -----------------------------

create_db()


# -----------------------------
# Upload configuration
# -----------------------------

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -----------------------------
# Home page
# -----------------------------

@app.route("/")
def home():
    return render_template("chatbot.html")


# -----------------------------
# Text claim analysis
# -----------------------------

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True)

    if not data or "message" not in data:
        return jsonify({
            "response": "Please enter a claim or message to analyze.",
            "references": []
        }), 400

    user_input = data["message"].strip()

    if not user_input:
        return jsonify({
            "response": "Please enter some text first.",
            "references": []
        }), 400

    # Search local misinformation database
    try:
        db_results = search_misinformation(user_input)
    except Exception as e:
        print("Database search error:", e)
        db_results = []

    # Send database references to Gemini
    result = get_response(
        user_input,
        reference_results=db_results
    )

    # Convert database rows into JSON-friendly objects
    references = []

    for row in db_results:
        references.append({
            "id": row[0],
            "title": row[1],
            "content": row[2],
            "verdict": row[3],
            "source": row[4],
            "category": row[5],
            "date_added": row[6]
        })

    return jsonify({
        "response": result,
        "references": references
    })


# -----------------------------
# Image analysis
# -----------------------------

@app.route("/analyze_image", methods=["POST"])
def analyze_image_route():

    if "file" not in request.files:
        return jsonify({
            "response": "No image uploaded.",
            "references": []
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "response": "Please select an image.",
            "references": []
        }), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    try:

        file.save(file_path)

        result = analyze_image(
            file_path,
            file.content_type
        )

        return jsonify({
            "response": result,
            "references": []
        })

    except Exception as e:

        print("Image route error:", e)

        return jsonify({
            "response": "Unable to analyze this image.",
            "references": []
        }), 500

    finally:

        if os.path.exists(file_path):
            os.remove(file_path)


# -----------------------------
# Audio analysis
# -----------------------------

@app.route("/analyze_audio", methods=["POST"])
def analyze_audio_route():

    if "file" not in request.files:
        return jsonify({
            "response": "No audio uploaded.",
            "references": []
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "response": "Please select an audio file.",
            "references": []
        }), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    try:

        file.save(file_path)

        result = analyze_audio(
            file_path,
            file.content_type
        )

        return jsonify({
            "response": result,
            "references": []
        })

    except Exception as e:

        print("Audio route error:", e)

        return jsonify({
            "response": "Unable to analyze this audio.",
            "references": []
        }), 500

    finally:

        if os.path.exists(file_path):
            os.remove(file_path)


# -----------------------------
# Video analysis
# -----------------------------

@app.route("/analyze_video", methods=["POST"])
def analyze_video_route():

    if "file" not in request.files:
        return jsonify({
            "response": "No video uploaded.",
            "references": []
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "response": "Please select a video.",
            "references": []
        }), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    try:

        file.save(file_path)

        result = analyze_video(
            file_path,
            file.content_type
        )

        return jsonify({
            "response": result,
            "references": []
        })

    except Exception as e:

        print("Video route error:", e)

        return jsonify({
            "response": "Unable to analyze this video.",
            "references": []
        }), 500

    finally:

        if os.path.exists(file_path):
            os.remove(file_path)


# -----------------------------
# Run application
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)








