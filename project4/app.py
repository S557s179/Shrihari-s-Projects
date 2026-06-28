from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory store (Render-safe for demo projects)
notes = {}
note_id_counter = 1


@app.route("/")
def home():
    return jsonify({
        "message": "Safe Notes API is running",
        "endpoints": ["/health", "/notes (GET, POST)", "/notes/<id> (GET, DELETE)"]
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


# CREATE NOTE
@app.route("/notes", methods=["POST"])
def create_note():
    global note_id_counter

    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' field"}), 400

        note = {
            "id": note_id_counter,
            "text": data["text"]
        }

        notes[note_id_counter] = note
        note_id_counter += 1

        return jsonify(note), 201

    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500


# GET ALL NOTES
@app.route("/notes", methods=["GET"])
def get_notes():
    return jsonify(list(notes.values())), 200


# GET SINGLE NOTE
@app.route("/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):
    note = notes.get(note_id)

    if not note:
        return jsonify({"error": "Note not found"}), 404

    return jsonify(note), 200


# DELETE NOTE
@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    if note_id not in notes:
        return jsonify({"error": "Note not found"}), 404

    del notes[note_id]
    return jsonify({"message": "Deleted successfully"}), 200


# GLOBAL ERROR HANDLER (prevents crashes)
@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)