-- DROP TABLE IF EXISTS Patients;
-- DROP TABLE IF EXISTS Appointment;
-- DROP TABLE IF EXISTS AppointmentInfo;
-- DROP TABLE IF EXISTS Doctor;
-- DROP TABLE IF EXISTS Hospital; 


CREATE TABLE Patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT NOT NULL,
    insurance TEXT NOT NULL

);

CREATE TABLE Doctor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    registration_number INTEGER NOT NULL,
    specilzation TEXT NOT NULL,
    hospital_id INTEGER,
    
    CONSTRAINT FK_hospital_id FOREIGN KEY (hospital_id)
    REFERENCES Hospital(id)
);

CREATE TABLE DoctorHospital (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER, 
    hospital_id INTEGER,
    
    CONSTRAINT FK_hospital_id FOREIGN KEY (hospital_id)
    REFERENCES Hospital(id)
);

CREATE TABLE Hospital(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospital_name TEXT NOT NULL,
    pincode TEXT NOT NULL
);

CREATE TABLE Appointment(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_time TIMESTAMP  NOT NULL,
    end_time TIMESTAMP NOT NULL,
    duration INTEGER NOT NULL,
    doctor_hospital_id INTEGER,
    CONSTRAINT FK_doctor_hospital_id FOREIGN KEY (doctor_hospital_id)
    REFERENCES DoctorHospital(id)

);

CREATE TABLE AppointmentInfo(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER,
    patient_id INTEGER NOT NULL,
    
    CONSTRAINT FK_patient_id FOREIGN KEY (patient_id)
    REFERENCES Patients(id),
    CONSTRAINT FK_appointment_id FOREIGN KEY (appointment_id)
    REFERENCES Appointment(id)
);

