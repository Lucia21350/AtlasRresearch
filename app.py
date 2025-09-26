from flask import Flask, request, jsonify
import os
from config import BASE_UPLOAD_DIR
from utils import save_and_extract_zip

app = Flask(__name__)

@app.route("/prediction", methods=["POST"])
def upload_zip():
    try:
        research_id = request.form.get("research_id")
        if not research_id:
            return jsonify({"error": "research_id is required"}), 400

        if "file" not in request.files:
            return jsonify({"error": "No file part in request"}), 400

        zip_file = request.files["file"]
        if zip_file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        target_dir = os.path.join(BASE_UPLOAD_DIR, research_id)
        extracted_path = save_and_extract_zip(zip_file, target_dir)

        return jsonify({
            "message": "File uploaded and extracted successfully",
            "extracted_path": extracted_path
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
