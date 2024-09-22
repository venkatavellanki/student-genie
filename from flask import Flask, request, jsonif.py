from flask import Flask, request, jsonify
import base64
import os
import magic
import string

app = Flask(__name__)

# Helper function to validate the Base64 file and retrieve its MIME type and size
def validate_base64_file(encoded_file):
    try:
        file_data = base64.b64decode(encoded_file)
        mime = magic.Magic(mime=True)
        mime_type = mime.from_buffer(file_data)
        file_size_kb = len(file_data) / 1024.0
        return True, mime_type, file_size_kb
    except Exception as e:
        return False, None, 0

# POST Method at /bfhl route
@app.route('/bfhl', methods=['POST'])
def handle_post():
    try:
        data = request.get_json()

        # Extracting fields from the JSON payload
        status = data.get('status', False)
        full_name = data.get('full_name', 'venkat_aditya')
        dob = data.get('dob', '23062003')  # Default format is DDMMYYYY
        college_email = data.get('college_email', '')
        college_roll = data.get('college_roll', '')
        numbers_array = data.get('numbers_array', [])
        alphabet_array = data.get('alphabet_array', [])
        base64_file = data.get('file', None)

        # Generate user_id from full_name and dob
        user_id = f"{full_name.lower()}_{dob}"

        # Identify the highest lowercase alphabet
        lowercase_letters = [char for char in alphabet_array if char in string.ascii_lowercase]
        highest_lowercase = max(lowercase_letters) if lowercase_letters else None

        # Validate the Base64 file if present
        file_valid = False
        file_mime_type = None
        file_size_kb = 0

        if base64_file:
            file_valid, file_mime_type, file_size_kb = validate_base64_file(base64_file)

        # Return the JSON response
        return jsonify({
            "is_success": status,
            "user_id": user_id,
            "college_email": college_email,
            "college_roll": college_roll,
            "numbers_array": numbers_array,
            "alphabet_array": alphabet_array,
            "highest_lowercase": highest_lowercase,
            "file": {
                "file_valid": file_valid,
                "file_mime_type": file_mime_type,
                "file_size_kb": file_size_kb
            }
        }), 200

    except Exception as e:
        return jsonify({
            "is_success": False,
            "message": "An error occurred",
            "error": str(e)
        }), 400

# GET Method at /bfhl route
@app.route('/bfhl', methods=['GET'])
def handle_get():
    # Hardcoded response for GET method
    response = {
        "operation_code": "BFHL2023"
    }
    return jsonify(response), 200

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
