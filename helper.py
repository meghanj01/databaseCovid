from flask import abort

def check_slots(db, request):
    # execution of db quries should be handled in try catch statements 
    #future scope club these 2 queries in one query
    try :
        query = f"""
                select a.id
                from Appointment a
                INNER JOIN DoctorHospital dh
                INNER JOIN Doctor d
                where a.start_time = {request['time']} and a.duration <= {request['duration']} 
                    and dh.doctor_id = d.id and d.spelization = {request['category']}
                """
        cur = db.cursor()
        cur.execute(query)
        result = cur.fetchone()
        if result :
            query = f""" insert into AppointmentInfo (appointment_id, patient_id) 
            values (result, {request['patient_id']})"""
            cur.execute(query)
            appointment_id = cur.fetchone()
            db.commit()
        abort('Sorry appointment is not available, please check the available slots again')
        cur.close()
        return appointment_id
    except Exception as ex:
        abort('Internal server error', 500)

def get_all_open_appointments(db):
    try :
        query = """ select * from  Appointment a LEFT JOIN AppointmentInfo ai ON a.id = ai.appointment_id"""
        cur = db.cursor()
        cur.execute(query)
        result = cur.fetchall()
        if not result:
            abort('No appointments available', 404)
        return result
    except Exception as ex:
        abort('Internal server error', 500)
        
        
    