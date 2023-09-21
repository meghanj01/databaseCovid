from flask import abort, make_response, jsonify
import db.db as database


def check_slots(db, request):
    """
    Check available appointment slots based on the request.

    Args:
    - db: Database connection.
    - request: JSON request data containing appointment details.

    Returns:
    - Appointment ID if a slot is available.
    - Raises an HTTP 500 error if there's an internal server error.
    - Raises an HTTP 400 error if no slots are available.
    """

    try:
        appointment_id = None
        # durations is number and in minutes
        # future scope club these 2 query into single query
        # query can be optimised further
        query = f"""
                INSERT INTO AppointmentInfo (appointment_id, patient_id)
                SELECT a.id, ?
                FROM Appointment a
                -- LEFT JOIN AppointmentInfo ai ON a.id = ai.appointment_id 
                INNER JOIN DoctorHospital dh ON a.doctor_hospital_id = dh.id 
                -- INNER JOIN Doctor d ON dh.doctor_id = d.id 
                WHERE 
                -- ai.appointment_id is null
                a.id not in (select appointment_id from AppointmentInfo)
                AND a.start_time = ?
                AND a.duration <= ?
                -- AND d.specilzation = ?
                """
        cur = db.cursor()
        cur.execute(
            query, (request["patient_id"], request["time"], int(request["duration"]))
        )
        result = cur.fetchone()
        appointment_id = cur.lastrowid
        db.commit()
        cur.close()
    except Exception as ex:
        abort(make_response(jsonify(message=f"Internal server error: {ex}"), 500))
    if appointment_id:
        return appointment_id
    abort(
        make_response(
            jsonify(
                message="Sorry, no appointment slots are  available. Please check the available slots again"
            ),
            404,
        )
    )


def get_all_open_appointments(db):
    """
    Retrieve a list of all open appointments.

    Args:
    - db: Database connection.

    Returns:
    - List of open appointment details.
    - Raises an HTTP 404 error if no appointments are available.
    """

    query = """SELECT
                a.start_time, a.end_time, a.duration, d.specilzation AS specilzation,
                h.hospital_name AS hospital_name, h.pincode AS pincode
                
                FROM Appointment a
                
                LEFT JOIN AppointmentInfo ai ON a.id = ai.appointment_id
                JOIN DoctorHospital dh ON a.doctor_hospital_id = dh.id
                JOIN Doctor d ON d.id = dh.doctor_id
                JOIN Hospital h ON h.id = dh.hospital_id
                WHERE ai.appointment_id is null
                """
    result = database.db_execute(db, query)
    if not result:
        abort(make_response(jsonify(message="No appointments available"), 404))
    return result


def get_appointment_id(db, id):
    """
    Retrieve an appointment by its ID.

    Args:
    - db: Database connection.
    - id: Appointment ID to retrieve.

    Returns:
    - Appointment details.
    - Raises an HTTP 400 error if the ID is incorrect.
    - Raises an HTTP 500 error if there's an internal server error.
    """

    try:
        query = f"""SELECT ai.id as id, p.patient_name, a.start_time, a.end_time, 
                a.duration, d.specilzation, h.hospital_name, h.pincode
                
                FROM AppointmentInfo ai
                JOIN Appointment a ON a.id = ai.appointment_id
                JOIN DoctorHospital dh ON dh.id = a.doctor_hospital_id
                JOIN Doctor d ON d.id = dh.doctor_id
                JOIN Hospital h ON h.id = dh.hospital_id
                JOIN Patients p ON ai.patient_id = p.id 
                
                WHERE ai.id = ?
                """

        cur = db.cursor()
        cur.execute(query, (id,))
        result = cur.fetchone()
        db.close()

        if result:
            return result

        abort(make_response(jsonify(message="Appointment ID is not correct"), 404))

    # more generalised exceptions we can use sql exceptions here
    except Exception as ex:
        db.close()
        abort(make_response(jsonify({"message": f"Internal server error: {ex}"}), 500))


def cancel_appointment_by_id(db, id):
    """
    Cancel an appointment by its ID.

    Args:
    - db: Database connection.
    - id: Appointment ID to cancel.

    Returns:
    - None.
    - Raises an HTTP 500 error if there's an internal server error.
    """

    try:
        query = f"DELETE FROM AppointmentInfo WHERE id = ?"
        cur = db.cursor()
        cur.execute(query, (id,))
        db.commit()
    except Exception as ex:
        abort(make_response(jsonify(message=f"Internal server error: {ex}"), 500))
