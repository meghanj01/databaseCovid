import sqlite3

# Open a connection to the SQLite database (my_database1.db)
connection = sqlite3.connect('my_database.db')

try:
    # Read and execute the schema from schema.sql
    with open('schema.sql') as f:
        connection.executescript(f.read())

    # Create a cursor for executing SQL statements
    cur = connection.cursor()

    # Insert data into tables
    cur.execute("""INSERT INTO Patients (patient_name, insurance) VALUES
                    ('John Doe', 'HealthCare Inc.'),
                    ('Jane Smith', 'MediCare Co.'),
                    ('Robert Johnson', 'Wellness Insurance');""")
    
    cur.execute("""INSERT INTO Appointment (start_time, end_time, duration, doctor_hospital_id) VALUES
                    ('2023-09-15 09:00:00', '2023-09-15 10:00:00', 60, 1),
                    ('2023-09-16 14:30:00', '2023-09-16 15:00:00', 30, 2),
                    ('2023-09-17 11:15:00', '2023-09-17 11:30:00', 15, 3);""")
    
    cur.execute("""INSERT INTO Doctor (registration_number, specilzation, hospital_id) VALUES
                    (12345, 'Cardiologist', 1),
                    (54321, 'Pediatrician', 2),
                    (67890, 'Dermatologist', 3);""")
    
    cur.execute("""INSERT INTO Hospital (hospital_name, pincode) VALUES
                    ('General Hospital', '12345'),
                    ('City Medical Center', '54321'),
                    ('Community Health Clinic', '67890');""")
    
    cur.execute("""INSERT INTO AppointmentInfo (appointment_id, patient_id) VALUES
                    (1, 1)""")
    
    # cur.execute("""DELETE FROM AppointmentInfo;""")

    cur.execute("""INSERT INTO DoctorHospital (doctor_id, hospital_id) VALUES
                    (1, 1),
                    (2, 2),
                    (3, 3),(1,2),(1,3),(2,2),(2,3),(3,1),(3,2);""")
    
    # Commit the changes
    connection.commit()
    
    # Fetch and print data from the database
    cur.execute("SELECT duration from Appointment;")
    durations = cur.fetchall()
    print("Durations in the database:")
    for duration in durations:
        print(duration[0])

except sqlite3.Error as e:
    print(f"SQLite error: {e}")

