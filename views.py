from flask import Flask, jsonify, request, Blueprint
import db.db as database
from validation import validate_post_request, validate_patient_profile, \
                    validate_appointment_id
from helper import check_slots, get_all_open_appointments, get_appointment_id, \
                    cancel_appointment_by_id

from flask import g

# Create a Flask blueprint
appointment = Blueprint('appointment', __name__)


# Route to create new appointments
@appointment.route('/', methods=['POST'])
def post_appointments():
    """
    Create a new appointment based on the provided JSON data.

    JSON Request Format:
    {
        "patient_name": "John Doe",
        "insurance": "HealthCare Inc.",
        "time": "2023-09-15 10:00:00",
        "duration": "1 hour",
        "category": "Category"
    }

    Returns:
    - JSON response with appointment booking status and details.
    """

    if request.method == 'POST' and request.is_json:
        db = database.get_db_connection()
        data = request.get_json()

        req = {
            'patient_name': data.get('patient_name'),
            'insurance': data.get('insurance'),
            'time': data.get('time'),
            'duration': data.get('duration'),
            'category': data.get('category')
        }

        req['patient_id'] = validate_patient_profile(db, req['patient_name'], req['insurance'])[0]
        validate_post_request(req)
        appointment_id = check_slots(db, req)
        
        database.close_db(db)

        return jsonify({'message': f'Your appointment is booked. Appointment number: {str(appointment_id)}. Please check the details by clicking on info.',
                            'status': 200})


# Route to get all open appointments
@appointment.route('/', methods=['GET'])
def get_appointments():
    """
    Retrieve a list of all open appointments.

    Returns:
    - JSON response with a list of open appointment details.
    """

    if request.method == 'GET':
        db = database.get_db_connection()
        result = get_all_open_appointments(db)
        database.close_db(db)

        appointment_data = []
        for res in result:
            appointment = {
                'start_time': res['start_time'],
                'end_time': res['end_time'],
                'duration': f"{res['duration']} minutes",
                'specialization': res['specilzation'],
                'hospital_name': res['hospital_name'],
                'pincode': res['pincode']
            }
            appointment_data.append(appointment)

        if result:
            return jsonify({'appointment_list': appointment_data, 'status_code': 200})
        
        return jsonify("No appointment available, sorry!")


# Route to get an appointment by ID
@appointment.route('/<int:id>', methods=['GET'])
def get_appointment_by_id(id):
    """
    Retrieve an appointment by its ID.

    Args:
    - id: The ID of the appointment to retrieve.

    Returns:
    - JSON response with appointment details.
    """

    if request.method == 'GET':
        db = database.get_db_connection()
        validate_appointment_id(db, id)
        res = get_appointment_id(db, id)
        database.close_db(db)

        appointment = {
            'appointment_id': res['id'],
            'patient_name': res['patient_name'],
            'start_time': res['start_time'],
            'duration': f"{res['duration']} minutes",
            'specialization': res['specilzation'],
            'hospital_name': res['hospital_name'],
            'pincode': res['pincode']
        }

        if appointment:
            return jsonify({'Appointment': appointment, 'status_code': 200})
        
        return jsonify("No appointment available, sorry!")


# Route to cancel an appointment by ID
@appointment.route('/<int:id>', methods=['DELETE'])
def cancel_appointment(id):
    """
    Cancel an appointment by its ID.

    Args:
    - id: The ID of the appointment to cancel.

    Returns:
    - JSON response indicating the status of the cancellation.
    """

    db = database.get_db_connection()
    validate_appointment_id(db, id)
    result = cancel_appointment_by_id(db, id)
    database.close_db(db)
    
    return jsonify({'message': 'Your appointment is cancelled successfully', 'status': 200})

# if __name__ == '__main__':
#     appointment.run(debug=True)
