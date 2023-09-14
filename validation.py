from flask import abort, make_response, jsonify
import config
from datetime import datetime

def validate_post_request(request):
    """
    Validate a POST request for creating a new appointment.

    Args:
    - request: JSON request data containing appointment details.

    Returns:
    - None: Raises an HTTP 400 error if validation fails.
    """
    if not request.get('time'):
        abort(make_response(jsonify(message = 'time is not given'), 400))

    try:
        datetime.strptime(request['time'], config.DT_FORMAT)
    except ValueError as ex:
        abort(make_response(jsonify(message = f'Invalid datetime {ex}'), 400))

    # Future scope for hour validation to handle partial slots
    # Convert duration to seconds
    if not request['duration'] or request['duration'] not in range(15, 60, 15):
        abort(make_response(jsonify( message = 'Invalid duration'), 400))

    if not request['category'] or request['category'] not in config.CATEGORY:
        abort(make_response(jsonify('Invalid category'), 400))

def validate_patient_profile(db, name, insurance):
    """
    Validate patient profile information.

    Args:
    - db: Database connection.
    - name: Patient's name.
    - insurance: Patient's insurance information.

    Returns:
    - Patient ID if the profile exists in the database.
    - Raises an HTTP 400 error if validation fails.
    """
    if name and insurance:
        query = f'SELECT id FROM Patients WHERE patient_name = "{name}" AND insurance = "{insurance}"'
        cur = db.cursor()
        cur.execute(query)
        result = cur.fetchone()
        cur.close()
        if not result :
            abort(make_response(jsonify(message = 'Patient record doesnot exists'), 400))
        return result
    abort(make_response(jsonify(message = 'Please enter Name and insurance'), 400))

def validate_appointment_id(db, id):
    """
    Validate an appointment ID.

    Args:
    - db: Database connection.
    - id: Appointment ID to validate.

    Returns:
    - Appointment ID if it exists in the database.
    - Raises an HTTP 400 error if validation fails.
    """
    try:
        query = f'SELECT id FROM AppointmentInfo WHERE id = {id}'
        cur = db.cursor()
        cur.execute(query)
        result = cur.fetchone()
      
    except Exception as ex:
        db.close()
        abort(make_response(jsonify(message = f'Internal server error {ex}'), 500))

    if result :
        return result
    else:
        abort(make_response(jsonify(message = 'Invalid appointment id, please check'), 404))
