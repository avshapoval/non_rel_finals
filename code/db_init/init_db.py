import time
import sys
import os
import logging

import pymongo


def setup_logger():
    logger = logging.getLogger('init_db')
    logger.setLevel(logging.INFO)
    
    return logger

def create_collections_with_schemas(db):
    
    # Студенты
    db.create_collection('students', validator={
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['studentId', 'firstName', 'lastName', 'email', 'faculty', 'enrollmentYear'],
            'properties': {
                'studentId': {
                    'bsonType': 'string',
                    'description': 'Уникальный идентификатор студента'
                },
                'firstName': {
                    'bsonType': 'string',
                    'description': 'Имя студента'
                },
                'lastName': {
                    'bsonType': 'string',
                    'description': 'Фамилия студента'
                },
                'email': {
                    'bsonType': 'string',
                    'description': 'Email студента',
                    'pattern': '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
                },
                'faculty': {
                    'bsonType': 'string',
                    'description': 'Название факультета'
                },
                'enrollmentYear': {
                    'bsonType': 'int',
                    'description': 'Год поступления',
                    'minimum': 2000,
                    'maximum': 2050
                },
                'dateOfBirth': {
                    'bsonType': 'date',
                    'description': 'Дата рождения студента'
                },
                'phoneNumber': {
                    'bsonType': 'string',
                    'description': 'Номер телефона студента'
                },
                'address': {
                    'bsonType': 'object',
                    'properties': {
                        'street': {'bsonType': 'string'},
                        'city': {'bsonType': 'string'},
                        'region': {'bsonType': 'string'},
                        'postalCode': {'bsonType': 'string'},
                        'country': {'bsonType': 'string'}
                    }
                }
            }
        }
    })
    
    # Курсы
    db.create_collection('courses', validator={
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['courseId', 'name', 'faculty', 'credits'],
            'properties': {
                'courseId': {
                    'bsonType': 'string',
                    'description': 'Уникальный идентификатор курса'
                },
                'name': {
                    'bsonType': 'string',
                    'description': 'Название курса'
                },
                'description': {
                    'bsonType': 'string',
                    'description': 'Описание курса'
                },
                'faculty': {
                    'bsonType': 'string',
                    'description': 'Название факультета'
                },
                'credits': {
                    'bsonType': 'int',
                    'description': 'Количество кредитов',
                    'minimum': 1,
                    'maximum': 10
                },
                'semester': {
                    'bsonType': 'string',
                    'description': 'Семестр, когда предлагается курс',
                    'enum': ['Осенний', 'Весенний', 'Летний', 'Зимний']
                }
            }
        }
    })
    
    # Преподаватели
    db.create_collection('professors', validator={
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['professorId', 'firstName', 'lastName', 'email', 'faculty'],
            'properties': {
                'professorId': {
                    'bsonType': 'string',
                    'description': 'Уникальный идентификатор преподавателя'
                },
                'firstName': {
                    'bsonType': 'string',
                    'description': 'Имя преподавателя'
                },
                'lastName': {
                    'bsonType': 'string',
                    'description': 'Фамилия преподавателя'
                },
                'email': {
                    'bsonType': 'string',
                    'description': 'Email преподавателя',
                    'pattern': '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
                },
                'faculty': {
                    'bsonType': 'string',
                    'description': 'Название факультета'
                },
                'department': {
                    'bsonType': 'string',
                    'description': 'Название кафедры'
                },
                'title': {
                    'bsonType': 'string',
                    'description': 'Академическое звание',
                    'enum': ['Ассистент', 'Доцент', 'Профессор', 'Преподаватель', 'Старший преподаватель']
                },
                'phoneNumber': {
                    'bsonType': 'string',
                    'description': 'Номер телефона преподавателя'
                }
            }
        }
    })
    
    # Оценки
    db.create_collection('grades', validator={
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['studentId', 'courseId', 'professorId', 'semester', 'academicYear', 'grade'],
            'properties': {
                'studentId': {
                    'bsonType': 'string',
                    'description': 'Ссылка на студента'
                },
                'courseId': {
                    'bsonType': 'string',
                    'description': 'Ссылка на курс'
                },
                'professorId': {
                    'bsonType': 'string',
                    'description': 'Ссылка на преподавателя'
                },
                'semester': {
                    'bsonType': 'string',
                    'description': 'Семестр',
                    'enum': ['Осенний', 'Весенний', 'Летний', 'Зимний']
                },
                'academicYear': {
                    'bsonType': 'string',
                    'description': 'Учебный год (например, 2023-2024)'
                },
                'grade': {
                    'bsonType': 'int',
                    'description': 'Оценка (1-10)',
                    'minimum': 1,
                    'maximum': 10
                },
                'dateRecorded': {
                    'bsonType': 'date',
                    'description': 'Дата записи оценки'
                },
                'comments': {
                    'bsonType': 'string',
                    'description': 'Комментарии преподавателя'
                }
            }
        }
    })
    
    # Факультеты
    db.create_collection('faculties', validator={
        '$jsonSchema': {
            'bsonType': 'object',
            'required': ['name', 'dean'],
            'properties': {
                'name': {
                    'bsonType': 'string',
                    'description': 'Название факультета'
                },
                'dean': {
                    'bsonType': 'string',
                    'description': 'Имя декана'
                },
                'departments': {
                    'bsonType': 'array',
                    'items': {
                        'bsonType': 'string'
                    },
                    'description': 'Список кафедр'
                },
                'location': {
                    'bsonType': 'string',
                    'description': 'Расположение корпуса факультета'
                },
                'contactEmail': {
                    'bsonType': 'string',
                    'description': 'Контактный email факультета'
                }
            }
        }
    })

def create_indexes(db):
    
    db.students.create_index([("studentId", pymongo.ASCENDING)], unique=True)
    db.students.create_index([("email", pymongo.ASCENDING)], unique=True)
    db.students.create_index([("faculty", pymongo.ASCENDING)])
    db.students.create_index([("lastName", pymongo.ASCENDING), ("firstName", pymongo.ASCENDING)])
    
    db.courses.create_index([("courseId", pymongo.ASCENDING)], unique=True)
    db.courses.create_index([("faculty", pymongo.ASCENDING)])
    db.courses.create_index([("name", pymongo.ASCENDING)])
    
    db.professors.create_index([("professorId", pymongo.ASCENDING)], unique=True)
    db.professors.create_index([("email", pymongo.ASCENDING)], unique=True)
    db.professors.create_index([("faculty", pymongo.ASCENDING)])
    db.professors.create_index([("lastName", pymongo.ASCENDING), ("firstName", pymongo.ASCENDING)])
    
    db.grades.create_index([
        ("studentId", pymongo.ASCENDING), 
        ("courseId", pymongo.ASCENDING), 
        ("semester", pymongo.ASCENDING), 
        ("academicYear", pymongo.ASCENDING)
    ], unique=True)

    db.grades.create_index([("courseId", pymongo.ASCENDING)])
    db.grades.create_index([("professorId", pymongo.ASCENDING)])
    db.grades.create_index([("academicYear", pymongo.ASCENDING), ("semester", pymongo.ASCENDING)])
    
    db.faculties.create_index([("name", pymongo.ASCENDING)], unique=True)

def drop_existing_collections(db):
    collections = db.list_collection_names()
    for collection in collections:
        db.drop_collection(collection)

def setup_logger():
    logger = logging.getLogger('generate_data')
    logger.setLevel(logging.INFO)
    
    return logger

def main():
    logger = setup_logger()

    # Параметры подключения к MongoDB из переменной окружения или по умолчанию
    mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/university')
    
    max_retries = 5
    
    for attempt in range(max_retries):
        logger.info(f"Попытка подключения к MongoDB (попытка {attempt + 1}/{max_retries})...")

        client = pymongo.MongoClient(mongo_uri)

        client.admin.command('ping')
        logger.info("Успешное подключение к MongoDB.")
        
        db_name = mongo_uri.split('/')[-1].split('?')[0]
        db = client[db_name]
        
        drop_existing_collections(db)
        
        create_collections_with_schemas(db)
        
        create_indexes(db)
        
        logger.info("Инициализация базы данных завершена успешно!")
        client.close()         


if __name__ == "__main__":
    main()