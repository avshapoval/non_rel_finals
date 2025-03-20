import random
import string
import datetime
import os

import logging
import pymongo

from faker import Faker

# Список факультетов
faculties = [
    {"name": "Информатика", "dean": "Профессор Андрей Иванов", "departments": ["Программная инженерия", "Наука о данных", "Кибербезопасность"], "location": "Корпус А", "contactEmail": "cs@university.ru"},
    {"name": "Математика", "dean": "Профессор Елена Смирнова", "departments": ["Чистая математика", "Прикладная математика", "Статистика"], "location": "Корпус Б", "contactEmail": "math@university.ru"},
    {"name": "Физика", "dean": "Профессор Сергей Петров", "departments": ["Теоретическая физика", "Экспериментальная физика", "Астрономия"], "location": "Корпус В", "contactEmail": "physics@university.ru"},
    {"name": "Экономика", "dean": "Профессор Ольга Васильева", "departments": ["Макроэкономика", "Микроэкономика", "Финансы"], "location": "Корпус Г", "contactEmail": "economics@university.ru"},
    {"name": "История", "dean": "Профессор Михаил Соколов", "departments": ["Древняя история", "Новейшая история", "История искусств"], "location": "Корпус Д", "contactEmail": "history@university.ru"}
]

# Список курсов по факультетам
courses_by_faculty = {
    "Информатика": [
        {"courseId": "ИНФ101", "name": "Введение в программирование", "description": "Базовые концепции программирования", "faculty": "Информатика", "credits": 5, "semester": "Осенний"},
        {"courseId": "ИНФ102", "name": "Структуры данных", "description": "Фундаментальные структуры данных", "faculty": "Информатика", "credits": 5, "semester": "Весенний"},
        {"courseId": "ИНФ201", "name": "Алгоритмы", "description": "Разработка и анализ алгоритмов", "faculty": "Информатика", "credits": 6, "semester": "Осенний"},
        {"courseId": "ИНФ301", "name": "Базы данных", "description": "Проектирование и реализация баз данных", "faculty": "Информатика", "credits": 5, "semester": "Весенний"},
        {"courseId": "ИНФ401", "name": "Машинное обучение", "description": "Введение в машинное обучение", "faculty": "Информатика", "credits": 7, "semester": "Осенний"}
    ],
    "Математика": [
        {"courseId": "МАТ101", "name": "Математический анализ I", "description": "Введение в математический анализ", "faculty": "Математика", "credits": 5, "semester": "Осенний"},
        {"courseId": "МАТ102", "name": "Математический анализ II", "description": "Продвинутый математический анализ", "faculty": "Математика", "credits": 5, "semester": "Весенний"},
        {"courseId": "МАТ201", "name": "Линейная алгебра", "description": "Векторы и матрицы", "faculty": "Математика", "credits": 5, "semester": "Осенний"},
        {"courseId": "МАТ301", "name": "Теория вероятностей", "description": "Основы теории вероятностей", "faculty": "Математика", "credits": 6, "semester": "Весенний"},
        {"courseId": "МАТ401", "name": "Теория чисел", "description": "Свойства целых чисел", "faculty": "Математика", "credits": 5, "semester": "Осенний"}
    ],
    "Физика": [
        {"courseId": "ФИЗ101", "name": "Механика", "description": "Классическая механика", "faculty": "Физика", "credits": 5, "semester": "Осенний"},
        {"courseId": "ФИЗ102", "name": "Электромагнетизм", "description": "Электричество и магнетизм", "faculty": "Физика", "credits": 5, "semester": "Весенний"},
        {"courseId": "ФИЗ201", "name": "Термодинамика", "description": "Тепло и энергия", "faculty": "Физика", "credits": 5, "semester": "Осенний"},
        {"courseId": "ФИЗ301", "name": "Квантовая механика", "description": "Введение в квантовую теорию", "faculty": "Физика", "credits": 7, "semester": "Весенний"},
        {"courseId": "ФИЗ401", "name": "Теория относительности", "description": "Теория относительности Эйнштейна", "faculty": "Физика", "credits": 6, "semester": "Осенний"}
    ],
    "Экономика": [
        {"courseId": "ЭКО101", "name": "Микроэкономика", "description": "Индивидуальное экономическое поведение", "faculty": "Экономика", "credits": 5, "semester": "Осенний"},
        {"courseId": "ЭКО102", "name": "Макроэкономика", "description": "Экономические явления в масштабах экономики", "faculty": "Экономика", "credits": 5, "semester": "Весенний"},
        {"courseId": "ЭКО201", "name": "Эконометрика", "description": "Статистические методы в экономике", "faculty": "Экономика", "credits": 6, "semester": "Осенний"},
        {"courseId": "ЭКО301", "name": "Международная экономика", "description": "Глобальные экономические системы", "faculty": "Экономика", "credits": 5, "semester": "Весенний"},
        {"courseId": "ЭКО401", "name": "Экономическое развитие", "description": "Рост в развивающихся странах", "faculty": "Экономика", "credits": 5, "semester": "Осенний"}
    ],
    "История": [
        {"courseId": "ИСТ101", "name": "Мировая история", "description": "Обзор мировой истории", "faculty": "История", "credits": 4, "semester": "Осенний"},
        {"courseId": "ИСТ102", "name": "История Европы", "description": "История Европы", "faculty": "История", "credits": 4, "semester": "Весенний"},
        {"courseId": "ИСТ201", "name": "Древние цивилизации", "description": "Изучение древних обществ", "faculty": "История", "credits": 5, "semester": "Осенний"},
        {"courseId": "ИСТ301", "name": "Современная мировая история", "description": "История с 1900 года по настоящее время", "faculty": "История", "credits": 5, "semester": "Весенний"},
        {"courseId": "ИСТ401", "name": "Историография", "description": "Изучение исторических текстов", "faculty": "История", "credits": 6, "semester": "Осенний"}
    ]
}

# Должности
academic_titles = ["Ассистент", "Доцент", "Профессор", "Преподаватель", "Старший преподаватель"]

def setup_logger():
    logger = logging.getLogger('generate_data')
    logger.setLevel(logging.INFO)
    
    return logger

def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + datetime.timedelta(days=random_number_of_days)

def main():
    logger = setup_logger()

    fake = Faker('ru_RU')
    fake_en = Faker('en_US')

    mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/university')
    logger.info(f"Подключение к MongoDB: {mongo_uri}")
    client = pymongo.MongoClient(mongo_uri)

    db_name = mongo_uri.split('/')[-1].split('?')[0]
    db = client[db_name]
    logger.info(f"Используется база данных: {db_name}")

    # Очистка существующих данных
    db.students.delete_many({})
    db.professors.delete_many({})
    db.courses.delete_many({})
    db.grades.delete_many({})
    db.faculties.delete_many({})
    
    logger.info("Генерация данных для университетской базы данных...")
    
    faculty_ids = []
    for faculty in faculties:
        result = db.faculties.insert_one(faculty)
        faculty_ids.append(result.inserted_id)
    logger.info(f"Вставлено {len(faculty_ids)} факультетов")
    
    all_courses = []
    for faculty_name, courses in courses_by_faculty.items():
        all_courses.extend(courses)
    
    course_ids = []
    for course in all_courses:
        result = db.courses.insert_one(course)
        course_ids.append(result.inserted_id)
    logger.info(f"Вставлено {len(course_ids)} курсов")
    
    # Генерация преподавателей (3-5 на факультет)
    professor_ids = []
    for faculty in faculties:
        num_professors = random.randint(3, 5)
        for _ in range(num_professors):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email_first_name = fake_en.first_name().lower()
            email_last_name = fake_en.last_name().lower()
            professor = {
                "professorId": ''.join(random.choices(string.ascii_uppercase, k=2)) + ''.join(random.choices(string.digits, k=3)),
                "firstName": first_name,
                "lastName": last_name,
                "email": f"{email_first_name.lower()}.{email_last_name.lower()}@university.ru",
                "faculty": faculty["name"],
                "department": random.choice(faculty["departments"]),
                "title": random.choice(academic_titles),
                "phoneNumber": fake.phone_number()
            }
            result = db.professors.insert_one(professor)
            professor_ids.append(professor["professorId"])
    logger.info(f"Вставлено {len(professor_ids)} преподавателей")
    
    # Генерация студентов (20-30 на факультет)
    student_ids = []
    for faculty in faculties:
        num_students = random.randint(20, 30)
        for _ in range(num_students):
            enrollment_year = random.randint(2018, 2024)
            first_name = fake.first_name()
            last_name = fake.last_name()
            email_first_name = fake_en.first_name().lower()
            email_last_name = fake_en.last_name().lower()
            student = {
                "studentId": ''.join(random.choices(string.ascii_uppercase, k=1)) + ''.join(random.choices(string.digits, k=6)),
                "firstName": first_name,
                "lastName": last_name,
                "email": f"{email_first_name.lower()}.{email_last_name.lower()}@student.university.ru",
                "faculty": faculty["name"],
                "enrollmentYear": enrollment_year,
                "dateOfBirth": random_date(datetime.datetime(1995, 1, 1), datetime.datetime(2005, 1, 1)),
                "phoneNumber": fake.phone_number(),
                "address": {
                    "street": fake.street_address(),
                    "city": fake.city(),
                    "region": fake.region(),
                    "postalCode": fake.postcode(),
                    "country": "Россия"
                }
            }
            result = db.students.insert_one(student)
            student_ids.append(student["studentId"])
    logger.info(f"Вставлено {len(student_ids)} студентов")
    
    # Генерация оценок
    academic_years = ["2021-2022", "2022-2023", "2023-2024"]
    semesters = ["Осенний", "Весенний", "Летний", "Зимний"]
    
    grades_count = 0
    for student_id in student_ids:
        student = db.students.find_one({"studentId": student_id})
        faculty_name = student["faculty"]
        
        faculty_courses = courses_by_faculty[faculty_name]
        
        faculty_professors = list(db.professors.find({"faculty": faculty_name}))
        
        num_grades = random.randint(5, 15)
        for _ in range(num_grades):
            course = random.choice(faculty_courses)
            professor = random.choice(faculty_professors)
            academic_year = random.choice(academic_years)
            semester = random.choice(semesters)
            
            # Генерация оценки (1-10)
            numeric_grade = random.randint(1, 10)
            
            # Проверка, существует ли уже такая оценка
            existing_grade = db.grades.find_one({
                "studentId": student_id,
                "courseId": course["courseId"],
                "semester": semester,
                "academicYear": academic_year
            })
            
            if not existing_grade:
                grade = {
                    "studentId": student_id,
                    "courseId": course["courseId"],
                    "professorId": professor["professorId"],
                    "semester": semester,
                    "academicYear": academic_year,
                    "grade": numeric_grade,
                    "dateRecorded": random_date(datetime.datetime(2021, 1, 1), datetime.datetime(2024, 6, 1)),
                    "comments": random.choice(["Отличная работа", "Хорошая работа", "Требуется улучшение", "Удовлетворительно", "Выдающаяся работа", ""]) if random.random() > 0.5 else ""
                }
                db.grades.insert_one(grade)
                grades_count += 1
    
    logger.info(f"Вставлено {grades_count} оценок")
    logger.info("Генерация данных завершена!")

if __name__ == "__main__":
    main()