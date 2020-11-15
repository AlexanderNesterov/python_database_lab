import psycopg2

def open_connection():
    global connection
    connection = psycopg2.connect(dbname = 'penalties', user = 'postgres', 
                            password = 'postgres', host = 'localhost', port = "5432")
    global cursor
    cursor = connection.cursor()
    return connection, cursor

def close_connection(connection, cursor):
    cursor.close()
    connection.close()

def init_database(connection, cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS driver (
            id INTEGER PRIMARY KEY, 
            first_name VARCHAR(128) NOT NULL, 
            last_name VARCHAR(128) NOT NULL,
            passport VARCHAR(11) UNIQUE NOT NULL,
            birthdate DATE NOT NULL, 
            registration VARCHAR(512) NOT NULL);
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS licence (
            id INTEGER PRIMARY KEY, 
            number VARCHAR(10) UNIQUE NOT NULL, 
            start_date DATE NOT NULL, 
            end_date DATE NOT NULL, 
            driver_id INTEGER NOT NULL REFERENCES driver(id) ON DELETE CASCADE);
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS car (
            id INTEGER PRIMARY KEY, 
            mark VARCHAR(32) NOT NULL, 
            number VARCHAR(6) UNIQUE NOT NULL, 
            registration_date DATE NOT NULL, 
            driver_id INTEGER NOT NULL REFERENCES driver(id) ON DELETE CASCADE);
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS insurance (
            id INTEGER PRIMARY KEY, 
            insurance_date DATE NOT NULL, 
            insurance_cost INTEGER NOT NULL,  
            car_id INTEGER NOT NULL REFERENCES car(id) ON DELETE CASCADE);
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS penalty (
            id INTEGER PRIMARY KEY, 
            description VARCHAR(1024) NOT NULL, 
            cost INTEGER NOT NULL);
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS penalty_car (
            id INTEGER PRIMARY KEY,
            penalty_id INTEGER NOT NULL REFERENCES penalty(id) ON DELETE CASCADE, 
            car_id INTEGER NOT NULL REFERENCES car(id) ON DELETE CASCADE,
            penalty_date DATE NOT NULL);
        """)

    cursor.execute("""
        CREATE SEQUENCE car_sequence INCREMENT 1 START 1;
        """)

    cursor.execute("""
        CREATE SEQUENCE driver_sequence INCREMENT 1 START 1;
        """)

    cursor.execute("""
        CREATE SEQUENCE insurance_sequence INCREMENT 1 START 1;
        """)

    cursor.execute("""
        CREATE SEQUENCE licence_sequence INCREMENT 1 START 1;
        """)

    cursor.execute("""
        CREATE SEQUENCE penalty_sequence INCREMENT 1 START 1;
        """)
    
    cursor.execute("""
        CREATE SEQUENCE penalty_car_sequence INCREMENT 1 START 1;
        """)

    connection.commit()

def insert_data(connection, cursor):
    cursor.execute("""
        INSERT INTO driver VALUES(nextval(\'driver_sequence\'), 'Aaron', 'Ramsey', '2003 943420' , '10-10-1980', 'London, Street 1');
        INSERT INTO driver VALUES(nextval(\'driver_sequence\'), 'Kieran', 'Tierney', '1999 203942', '21-08-1991', 'Moscow, Street 2');
        INSERT INTO driver VALUES(nextval(\'driver_sequence\'), 'Bernd', 'Leno', '2004 203294', '14-03-1978', 'Paris, Street 4');
        INSERT INTO driver VALUES(nextval(\'driver_sequence\'), 'Hector', 'Bellerin', '1980 203023', '01-12-1983', 'Munich, Street 10');
        INSERT INTO driver VALUES(nextval(\'driver_sequence\'), 'Nicolas', 'Pepe', '2007 839403', '23-07-1989', 'Berlin, Street 14');
    """)
    
    cursor.execute("""
        INSERT INTO licence VALUES(nextval(\'licence_sequence\'), '1094857384', '12-10-2013', '12-10-2023', 1);
        INSERT INTO licence VALUES(nextval(\'licence_sequence\'), '8960458341', '07-01-2011', '07-01-2021', 2);
        INSERT INTO licence VALUES(nextval(\'licence_sequence\'), '9058694534', '24-12-2016', '24-12-2026', 3);
        INSERT INTO licence VALUES(nextval(\'licence_sequence\'), '4968048592', '01-03-2015', '01-03-2025', 4);
        INSERT INTO licence VALUES(nextval(\'licence_sequence\'), '9683069485', '25-06-2018', '25-06-2028', 5);
    """)

    cursor.execute("""
        INSERT INTO car VALUES(nextval(\'car_sequence\'), 'Toyota Corolla', 'md232k', '15-09-2013', 1);
        INSERT INTO car VALUES(nextval(\'car_sequence\'), 'Toyota Land Cruiser', 'lo254p', '07-12-2010', 1);
        INSERT INTO car VALUES(nextval(\'car_sequence\'), 'Lada Granta', 'bf490g', '01-11-2018', 2);
        INSERT INTO car VALUES(nextval(\'car_sequence\'), 'Hyundai Solaris', 'as231g', '03-07-2015', 4);
        INSERT INTO car VALUES(nextval(\'car_sequence\'), 'Jeep Wrangler', 'ui769j', '27-01-2008', 5);
        INSERT INTO car VALUES(nextval(\'car_sequence\'), 'Tesla Model X', 'er457h', '23-08-2019', 2);
    """)

    cursor.execute("""
        INSERT INTO penalty VALUES(nextval(\'penalty_sequence\'), 'Превышение скорости', 500);
        INSERT INTO penalty VALUES(nextval(\'penalty_sequence\'), 'Парковка в неположенном месте', 1000);
        INSERT INTO penalty VALUES(nextval(\'penalty_sequence\'), 'Вождение в нетрезвом виде', 5000);
        INSERT INTO penalty VALUES(nextval(\'penalty_sequence\'), 'Пересечение двух сплошных', 7000);
    """)

    cursor.execute("""
        INSERT INTO insurance VALUES(nextval(\'insurance_sequence\'), '12-01-2019', 15000, 1);
        INSERT INTO insurance VALUES(nextval(\'insurance_sequence\'), '02-10-2020', 20000, 2);
        INSERT INTO insurance VALUES(nextval(\'insurance_sequence\'), '23-08-2019', 7000, 4);
        INSERT INTO insurance VALUES(nextval(\'insurance_sequence\'), '14-04-2020', 12000, 6);
    """)

    cursor.execute("""
        INSERT INTO penalty_car VALUES(nextval(\'penalty_car_sequence\'), 1, 2, '12-10-2020');
        INSERT INTO penalty_car VALUES(nextval(\'penalty_car_sequence\'), 2, 4, '07-01-2019');
        INSERT INTO penalty_car VALUES(nextval(\'penalty_car_sequence\'), 3, 5, '23-05-2018');
        INSERT INTO penalty_car VALUES(nextval(\'penalty_car_sequence\'), 1, 6, '19-02-2020');
        INSERT INTO penalty_car VALUES(nextval(\'penalty_car_sequence\'), 2, 6, '21-09-2017');
        INSERT INTO penalty_car VALUES(nextval(\'penalty_car_sequence\'), 1, 3, '15-04-2019');
        INSERT INTO penalty_car VALUES(nextval(\'penalty_car_sequence\'), 1, 2, '31-08-2016');
    """)

    connection.commit()

def get_drivers():
    cursor.execute("""
        SELECT * FROM driver;
    """)
    return cursor.fetchall()

def get_driver_by_id(driver_id):
    cursor.execute("""
        SELECT * FROM driver
        WHERE id = {}
    """.format(driver_id))
    return cursor.fetchone()

def get_licence_by_driver_id(driver_id):
    cursor.execute("""
        SELECT * FROM licence
        WHERE driver_id = {}
    """.format(driver_id))
    return cursor.fetchone()

def get_penalties_by_car_ids(car_ids):
    cursor.execute("""
        SELECT mark, number, penalty_date, description, cost
        FROM penalty_car
        JOIN penalty ON penalty_car.penalty_id = penalty.id
        JOIN car ON penalty_car.car_id = car.id
        WHERE car.id IN ({});
    """.format(car_ids))
    return cursor.fetchall()

def get_cars_by_driver_id(driver_id):
    cursor.execute("""
        SELECT car.id, car.mark, car.number, car.registration_date, driver.first_name, driver.last_name 
        FROM car JOIN driver ON car.driver_id = driver.id 
        WHERE driver_id = {};
    """.format(driver_id))
    return cursor.fetchall()

def get_penalties():
    cursor.execute("""
        SELECT * FROM penalty;
    """)
    return cursor.fetchall()

def get_driver_by_passport(passport):
    cursor.execute("""
        SELECT * FROM driver
        WHERE passport = '{}'
    """.format(passport))
    return cursor.fetchone()

def insert_driver(first_name, last_name, passport, registration, birthdate):
    cursor.execute("""
        INSERT INTO driver VALUES(nextval(\'driver_sequence\'), '{}', '{}', '{}', '{}', '{}');
    """.format(first_name, last_name, passport, registration, birthdate))
    connection.commit()

def get_car_by_number(number):
    cursor.execute("""
        SELECT * FROM car
        WHERE number = '{}'
    """.format(number))
    return cursor.fetchone()

def insert_car(mark, number, registration_date, driver_id):
    cursor.execute("""
        INSERT INTO car VALUES(nextval(\'car_sequence\'), '{}', '{}', '{}', {});
    """.format(mark, number, registration_date, driver_id))
    connection.commit()

def insert_insurance(insurance_cost, insurance_date, car_id):
    cursor.execute("""
        INSERT INTO insurance VALUES(nextval(\'insurance_sequence\'), '{}', '{}', {});
    """.format(insurance_cost, insurance_date, car_id))
    connection.commit()

def update_driver(driver_id, first_name, last_name, passport, registration, birthdate):
    cursor.execute("""
        UPDATE driver SET first_name = '{}', last_name = '{}', passport = '{}', registration = '{}', birthdate = '{}'
        WHERE id = {}
    """.format(first_name, last_name, passport, registration, birthdate, driver_id))
    connection.commit()

def get_penalties_with_info():
    cursor.execute("""
        SELECT penalty_car.id, car.number, penalty_date, description, car.mark, penalty.cost, driver.first_name, driver.last_name 
        FROM penalty_car
        JOIN penalty ON penalty_car.penalty_id = penalty.id
        JOIN car ON penalty_car.car_id = car.id
        JOIN driver ON car.driver_id = driver.id;
    """)
    return cursor.fetchall()

def get_cars():
    cursor.execute("""
        SELECT * FROM car;
    """)
    return cursor.fetchall()

def insert_penalty_car(penalty_id, car_id, date):
    cursor.execute("""
        INSERT INTO penalty_car VALUES({}, {}, '{}');
    """.format(penalty_id, car_id, date))
    connection.commit()

def get_cars_with_insurance():
    cursor.execute("""
        SELECT car.id, mark, car.number, registration_date, insurance.id, insurance_date, insurance_cost 
        FROM car
        LEFT JOIN insurance ON car.id = insurance.car_id;
    """)
    return cursor.fetchall()

def insert_insurance_car(insurance_date, insurance_cost, car_id):
    cursor.execute("""
        INSERT INTO insurance VALUES(nextval(\'insurance_sequence\'), '{}', '{}', {});
    """.format(insurance_date, insurance_cost, car_id))
    connection.commit()

def get_drivers_with_licence():
    cursor.execute("""
        SELECT driver.id, first_name, last_name, passport, licence.id, licence.number, start_date, end_date
        FROM driver
        LEFT JOIN licence ON driver.id = licence.driver_id;
    """)
    return cursor.fetchall()

def get_driver_by_licence(licence_number):
    cursor.execute("""
        SELECT * FROM licence
        WHERE number = '{}'
    """.format(licence_number))
    return cursor.fetchone()

def insert_licence(number, start_date, end_date, driver_id):
    cursor.execute("""
        INSERT INTO licence VALUES(nextval(\'licence_sequence\'), '{}', '{}', '{}', {});
    """.format(number, start_date, end_date, driver_id))
    connection.commit()

def remove_driver_by_id(driver_id):
    cursor.execute("""
        DELETE FROM driver
        WHERE id = {}
    """.format(driver_id))
    connection.commit()

def remove_car_by_id(car_id):
    cursor.execute("""
        DELETE FROM car
        WHERE id = {}
    """.format(car_id))
    connection.commit()

def remove_insurance_by_id(insurance_id):
    cursor.execute("""
        DELETE FROM insurance
        WHERE id = {}
    """.format(insurance_id))
    connection.commit()

def remove_licence_by_id(licence_id):
    cursor.execute("""
        DELETE FROM licence
        WHERE id = {}
    """.format(licence_id))
    connection.commit()

def remove_penalty_car_by_id(penalty_car_id):
    cursor.execute("""
        DELETE FROM penalty_car
        WHERE id = {}
    """.format(penalty_car_id))
    connection.commit()

def remove_penalty_by_id(penalty_id):
    cursor.execute("""
        DELETE FROM penalty
        WHERE id = {}
    """.format(penalty_id))
    connection.commit()

def insert_penalty(description, cost):
    cursor.execute("""
        INSERT INTO penalty VALUES(nextval(\'penalty_sequence\'), '{}', {});
    """.format(description, cost))
    connection.commit()
