from flask import Blueprint, g
from db import db
from validation import validate_post_request, validate_patient_profile, get_all_open_appointments
from helper import check_slots
from flask.response import jonsify
appointment = Blueprint('appointment', __name__)

@appointment.route('/', methods = ['POST','GET'])
def get_post_appointments(request):
    db = db.get_connection()
    if request.method == 'POST':
        req = {
            'patient_name' : request.get('patient_name'),
            'registration_number' : request.get('registration_number'),
            'time': request.get('preffered_time'),
            'duration': request.get('duration'),
            'category': request.get('category')
        }
        req['paitent_id'] = validate_patient_profile(db, req['patient_name'], req['registration_number'])
        validate_post_request(db, req)
        appointment_id = check_slots(req)
        return jonsify('your appointment is booked {appointment_id} Please checck the details by clicking on info ', status = 200)

    if request.method == 'GET':
        #may need to conver to dictionary
        return jonsify(get_all_open_appointments(db), status = 200)
        