// Найти всех студентов определенного факультета (с сортировкой по фамилии)
db.students.find({ faculty: "Информатика" }).sort({ lastName: 1, firstName: 1 })

// Найти средний балл по конкретному курсу
db.grades.aggregate([
  { $match: { courseId: "ИНФ101" } },
  { $group: { _id: "$courseId", средний_балл: { $avg: "$grade" } } }
])

// Найти все курсы, которые преподает конкретный преподаватель
db.grades.aggregate([
  { $match: { professorId: "АБ123" } }, 
  { $group: { _id: "$courseId" } },
  { $lookup: {
      from: "courses",
      localField: "_id",
      foreignField: "courseId",
      as: "курс"
    }
  },
  { $unwind: "$курс" },
  { $project: { 
      _id: 0, 
      courseId: "$курс.courseId", 
      название: "$курс.name", 
      факультет: "$курс.faculty",
      семестр: "$курс.semester"
    } 
  }
])

// Найти ТОП-5 студентов с наивысшим средним баллом
db.grades.aggregate([
  { $group: { 
      _id: "$studentId", 
      средний_балл: { $avg: "$grade" } 
    } 
  },
  { $sort: { средний_балл: -1 } },
  { $limit: 5 },
  { $lookup: {
      from: "students",
      localField: "_id",
      foreignField: "studentId",
      as: "студент"
    }
  },
  { $unwind: "$студент" },
  { $project: {
      _id: 0,
      студент: { $concat: ["$студент.lastName", " ", "$студент.firstName"] },
      факультет: "$студент.faculty",
      средний_балл: 1
    }
  }
])

// Подсчитать количество студентов по факультетам
db.students.aggregate([
  { $group: { _id: "$faculty", количество_студентов: { $sum: 1 } } },
  { $sort: { количество_студентов: -1 } }
])

// Найти курсы с наибольшим процентом неудовлетворительных оценок (ниже 4)
db.grades.aggregate([
  { $group: {
      _id: "$courseId",
      всего_оценок: { $sum: 1 },
      неуд_оценок: {
        $sum: { $cond: [{ $lt: ["$grade", 4] }, 1, 0] }
      }
    }
  },
  { $match: { всего_оценок: { $gt: 5 } } },
  { $project: {
      _id: 1,
      всего_оценок: 1,
      неуд_оценок: 1,
      процент_неуд: {
        $multiply: [
          { $divide: ["$неуд_оценок", "$всего_оценок"] },
          100
        ]
      }
    }
  },
  { $sort: { процент_неуд: -1 } },
  { $limit: 10 },
  { $lookup: {
      from: "courses",
      localField: "_id",
      foreignField: "courseId",
      as: "курс"
    }
  },
  { $unwind: "$курс" },
  { $project: {
      _id: 0,
      курс: "$курс.name",
      факультет: "$курс.faculty",
      всего_оценок: 1,
      неуд_оценок: 1,
      процент_неуд: 1
    }
  }
])

// Найти все оценки конкретного студента с информацией о курсах
db.grades.aggregate([
  { $match: { studentId: "С123456" } }, 
  { $lookup: {
      from: "courses",
      localField: "courseId",
      foreignField: "courseId",
      as: "курс"
    }
  },
  { $unwind: "$курс" },
  { $lookup: {
      from: "professors",
      localField: "professorId",
      foreignField: "professorId",
      as: "преподаватель"
    }
  },
  { $unwind: "$преподаватель" },
  { $project: {
      _id: 0,
      курс: "$курс.name",
      семестр: "$semester",
      учебный_год: "$academicYear",
      оценка: "$grade",
      преподаватель: { $concat: ["$преподаватель.lastName", " ", "$преподаватель.firstName"] }
    }
  },
  { $sort: { учебный_год: -1, семестр: 1 } }
])

// Сравнение среднего балла по факультетам
db.grades.aggregate([
  { $lookup: {
      from: "students",
      localField: "studentId",
      foreignField: "studentId",
      as: "студент"
    }
  },
  { $unwind: "$студент" },
  { $group: {
      _id: "$студент.faculty",
      средний_балл: { $avg: "$grade" },
      макс_оценка: { $max: "$grade" },
      мин_оценка: { $min: "$grade" }
    }
  },
  { $sort: { средний_балл: -1 } }
])

// Найти преподавателей, которые ставят самые высокие и низкие оценки
db.grades.aggregate([
  { $group: {
      _id: "$professorId",
      средняя_оценка: { $avg: "$grade" },
      количество_оценок: { $sum: 1 }
    }
  },
  { $match: { количество_оценок: { $gt: 5 } } }, 
  { $sort: { средняя_оценка: -1 } },
  { $lookup: {
      from: "professors",
      localField: "_id",
      foreignField: "professorId",
      as: "преподаватель"
    }
  },
  { $unwind: "$преподаватель" },
  { $project: {
      _id: 0,
      преподаватель: { $concat: ["$преподаватель.lastName", " ", "$преподаватель.firstName"] },
      должность: "$преподаватель.title",
      факультет: "$преподаватель.faculty",
      средняя_оценка: 1,
      количество_оценок: 1
    }
  }
])

// Распределение оценок по семестрам
db.grades.aggregate([
  { $group: {
      _id: { семестр: "$semester", учебный_год: "$academicYear" },
      средний_балл: { $avg: "$grade" },
      количество_оценок: { $sum: 1 },
      распределение: {
        $push: "$grade"
      }
    }
  },
  { $addFields: {
      распределение_оценок: {
        "10": { $size: { $filter: { input: "$распределение", as: "оценка", cond: { $eq: ["$$оценка", 10] } } } },
        "9": { $size: { $filter: { input: "$распределение", as: "оценка", cond: { $eq: ["$$оценка", 9] } } } },
        "8": { $size: { $filter: { input: "$распределение", as: "оценка", cond: { $eq: ["$$оценка", 8] } } } },
        "7": { $size: { $filter: { input: "$распределение", as: "оценка", cond: { $eq: ["$$оценка", 7] } } } },
        "6": { $size: { $filter: { input: "$распределение", as: "оценка", cond: { $eq: ["$$оценка", 6] } } } },
        "5": { $size: { $filter: { input: "$распределение", as: "оценка", cond: { $eq: ["$$оценка", 5] } } } },
        "4": { $size: { $filter: { input: "$распределение", as: "оценка", cond: { $eq: ["$$оценка", 4] } } } },
        "3": { $size: { $filter: { input: "$распределение", as: "оценка", cond: { $eq: ["$$оценка", 3] } } } },
        "2": { $size: { $filter: { input: "$распределение", as: "оценка", cond: { $eq: ["$$оценка", 2] } } } },
        "1": { $size: { $filter: { input: "$распределение", as: "оценка", cond: { $eq: ["$$оценка", 1] } } } }
      }
    }
  },
  { $project: {
      _id: 0,
      учебный_год: "$_id.учебный_год",
      семестр: "$_id.семестр",
      средний_балл: 1,
      количество_оценок: 1,
      распределение_оценок: 1
    }
  },
  { $sort: { учебный_год: -1, семестр: 1 } }
])

// Найти курсы с самым высоким и низким средним баллом
db.grades.aggregate([
  { $group: {
      _id: "$courseId",
      средний_балл: { $avg: "$grade" },
      количество_оценок: { $sum: 1 }
    }
  },
  { $match: { количество_оценок: { $gt: 5 } } }, 
  { $sort: { средний_балл: -1 } },
  { $lookup: {
      from: "courses",
      localField: "_id",
      foreignField: "courseId",
      as: "курс"
    }
  },
  { $unwind: "$курс" },
  { $project: {
      _id: 0,
      курс: "$курс.name",
      идентификатор: "$курс.courseId",
      факультет: "$курс.faculty",
      средний_балл: 1,
      количество_оценок: 1
    }
  }
])

// Среднегодовая статистика успеваемости по факультетам
db.grades.aggregate([
  { $lookup: {
      from: "students",
      localField: "studentId",
      foreignField: "studentId",
      as: "студент"
    }
  },
  { $unwind: "$студент" },
  { $group: {
      _id: {
        факультет: "$студент.faculty",
        год: "$academicYear"
      },
      средний_балл: { $avg: "$grade" },
      количество_оценок: { $sum: 1 }
    }
  },
  { $sort: { "_id.год": -1, "_id.факультет": 1 } },
  { $project: {
      _id: 0,
      факультет: "$_id.факультет",
      учебный_год: "$_id.год",
      средний_балл: 1,
      количество_оценок: 1
    }
  }
]) 