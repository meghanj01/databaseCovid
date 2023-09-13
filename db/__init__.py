import sqlite3

connection = sqlite3.connect(':memory:') 

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("""INSERT INTO Patients (patient_name, insurance) 
            VALUES ('John Doe', 'ABC'), 
                ('Jane Smith', 'XYZ'),
                ('Robert Johnson', '123');"""
            )

cur.execute("""INSERT INTO Appointment (start_time, end_time, duration)
            VALUES ('2023-09-15 10:00:00', '2023-09-15 10:15:00', '15 minutes'),
            ('2023-09-16 14:30:00', '2023-09-16 15:00:00', '30 minutes'),
            ('2023-09-17 09:15:00', '2023-09-17 10:15:00', '1 hour');"""
            )

cur.execute("""INSERT INTO Doctor (registration_number, specilzation, hospital_id)
                VALUES 
                (12345, 'Cardiologist', 1),
                (67890, 'Pediatrician', 1),
                (54321, 'Orthopedic Surgeon', 2);"""
            )

cur.execute("""INSERT INTO Hospital (hospital_name, pincode)
                VALUES ('St. John Hospital', '12345'),
                ('City General Hospital', '67890');"""
            )

connection.commit()
connection.close()