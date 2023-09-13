from flask import abort
import config
def validate_post_request(request):
    if not request['time'] or not request['time'].strptime(config.DT_FORMAT) :
        abort('Invalid time', 400)

    #future scope for hour validation to handle partial slots
    #convert duration in seconds
    if not request['duration'] or request['durations'].lower() not in ['1 hour', '30 minutes', '15 minutes']:
        abort('Invalid duration', 400)
    
    if not request['category'] or request['category'] not in config.CATEGORY:
        abort('Invalid category')
    return

    


def validate_patient_profile(db, name, insurance):
    if name and insurance:
        query = f'select id from Patient where patient_name = {name} and insurance = {insurance}'
        cur = db.cursor()
        cur.execute(query)
        result = cur.fetchone()
        if not result :
            abort('Patient record doesnot exists')
        return result

        

