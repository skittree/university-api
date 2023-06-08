# University API (Полимедика)

The following repository contains a university management schema and a FastAPI implementation of it. Created for a job position.

## Tasks

### 1. UML Class (ER Diagram)

You can access the [diagrams](https://drive.google.com/file/d/1SXw5WxPxwkkTuPkcA8vg4nhze4KFbY_i/view?usp=sharing) in draw.io.

![uml_class](https://github.com/skittree/university-api/assets/32728173/402f51a7-51f0-4b61-add4-5eae4c7e5d3b)
![er_dbeaver](https://github.com/skittree/university-api/assets/32728173/cd140625-4eca-4307-959c-7c378df62c91)

### 2. SQL Requests

#### Table Creation

```sql
CREATE TABLE faculties (
    id SERIAL NOT NULL, 
    code VARCHAR NOT NULL, 
    name VARCHAR NOT NULL, 
    PRIMARY KEY (id)
)

CREATE TABLE classes (
    id SERIAL NOT NULL, 
    name VARCHAR NOT NULL, 
    PRIMARY KEY (id)
)

CREATE TABLE exams (
    id SERIAL NOT NULL, 
    name VARCHAR NOT NULL, 
    PRIMARY KEY (id)
)

CREATE TABLE departments (
    id SERIAL NOT NULL, 
    faculty_id INTEGER NOT NULL, 
    name VARCHAR NOT NULL, 
    "desc" VARCHAR, 
    url VARCHAR, 
    PRIMARY KEY (id), 
    FOREIGN KEY(faculty_id) REFERENCES faculties (id)
)

CREATE TABLE professors (
    id SERIAL NOT NULL, 
    department_id INTEGER NOT NULL, 
    name VARCHAR NOT NULL, 
    phone VARCHAR, 
    address VARCHAR, 
    PRIMARY KEY (id), 
    FOREIGN KEY(department_id) REFERENCES departments (id)
)

CREATE TABLE groups (
    id SERIAL NOT NULL, 
    department_id INTEGER NOT NULL, 
    enrolled_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(department_id) REFERENCES departments (id)
)

CREATE TABLE curriculums (
    id SERIAL NOT NULL, 
    department_id INTEGER NOT NULL, 
    name VARCHAR NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(department_id) REFERENCES departments (id)
)
 
CREATE TABLE buildings (
    id SERIAL NOT NULL, 
    department_id INTEGER, 
    address VARCHAR NOT NULL, 
    name VARCHAR NOT NULL, 
    floors INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(department_id) REFERENCES departments (id)
)

CREATE TABLE students (
    id SERIAL NOT NULL, 
    group_id INTEGER NOT NULL, 
    name VARCHAR NOT NULL, 
    phone VARCHAR, 
    address VARCHAR, 
    PRIMARY KEY (id), 
    FOREIGN KEY(group_id) REFERENCES groups (id)
)

CREATE TABLE semesters (
    id SERIAL NOT NULL, 
    curriculum_id INTEGER NOT NULL, 
    start TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    "end" TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(curriculum_id) REFERENCES curriculums (id)
)

CREATE TABLE auditoriums (
    id SERIAL NOT NULL, 
    building_id INTEGER NOT NULL, 
    room_number INTEGER NOT NULL, 
    floor INTEGER, 
    max_capacity INTEGER, 
    has_projector BOOLEAN NOT NULL, 
    has_board BOOLEAN NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(building_id) REFERENCES buildings (id)
)

CREATE TABLE courses (
    id SERIAL NOT NULL, 
    semester_id INTEGER, 
    name VARCHAR NOT NULL, 
    "desc" VARCHAR, 
    PRIMARY KEY (id), 
    FOREIGN KEY(semester_id) REFERENCES semesters (id)
)

CREATE TABLE timeslots (
    id SERIAL NOT NULL, 
    auditorium_id INTEGER NOT NULL, 
	course_id INTEGER,
    class_id INTEGER, 
    exam_id INTEGER, 
    start TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    "end" TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (class_id), 
    UNIQUE (exam_id), 
    FOREIGN KEY(auditorium_id) REFERENCES auditoriums (id), 
	FOREIGN KEY(course_id) REFERENCES courses (id),
    FOREIGN KEY(class_id) REFERENCES classes (id), 
    FOREIGN KEY(exam_id) REFERENCES exams (id)
)

CREATE TABLE course_students (
    course_id INTEGER NOT NULL, 
    student_id INTEGER NOT NULL, 
    PRIMARY KEY (course_id, student_id), 
    FOREIGN KEY(course_id) REFERENCES courses (id), 
    FOREIGN KEY(student_id) REFERENCES students (id)
)

CREATE TABLE course_professors (
    course_id INTEGER NOT NULL, 
    professor_id INTEGER NOT NULL, 
    PRIMARY KEY (course_id, professor_id), 
    FOREIGN KEY(course_id) REFERENCES courses (id), 
    FOREIGN KEY(professor_id) REFERENCES professors (id)
)

CREATE TABLE tasks (
    id SERIAL NOT NULL, 
    course_id INTEGER NOT NULL, 
    name VARCHAR NOT NULL, 
    "desc" VARCHAR, 
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    deadline TIMESTAMP WITHOUT TIME ZONE, 
    PRIMARY KEY (id), 
    FOREIGN KEY(course_id) REFERENCES courses (id)
)

CREATE TABLE grades (
    id SERIAL NOT NULL, 
    student_id INTEGER NOT NULL, 
    grade INTEGER NOT NULL, 
    task_id INTEGER, 
    exam_id INTEGER, 
    course_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(student_id) REFERENCES students (id), 
    FOREIGN KEY(task_id) REFERENCES tasks (id), 
    FOREIGN KEY(exam_id) REFERENCES exams (id), 
    FOREIGN KEY(course_id) REFERENCES courses (id)
)
```

#### Select students on "Математика" course

```sql
SELECT s.id, s.name
FROM students s
JOIN course_students cs ON s.id = cs.student_id
JOIN courses c ON cs.course_id = c.id
WHERE c.name = 'Математика';
-- alternative that ensures the semester hasn't ended
SELECT s.id, s.name
FROM students s
JOIN course_students cs ON s.id = cs.student_id
JOIN courses c ON cs.course_id = c.id
JOIN semesters sem ON c.semester_id = sem.id
WHERE c.name = 'Математика' AND sem."end" <= now();
```

#### Update grade via student_id and course_id

```sql
UPDATE grades
SET grade = 5
WHERE student_id = 1
  AND course_id = 2;
```

#### Select all professors working at "Здание №3"
```sql
SELECT p.id, p.name
FROM professors p
JOIN departments d ON p.department_id = d.id
JOIN buildings b ON b.department_id = d.id
WHERE b.name = 'Здание №3';
```

#### Delete all tasks older than a year

```sql
DELETE FROM tasks WHERE created_at < now() - interval '1 year'
```

#### Add semester

```sql
INSERT INTO semesters (curriculum_id, "start", "end")
VALUES (1, '2017-01-14', '2017-04-01');
```

## Installation

### **Docker**

This method allows for an easy installation of both the PostgreSQL database and API using Docker containers.

1. Make sure to have [**Docker**](https://www.docker.com) installed and running with **Compose** on your local machine before setup. Use Linux containers.

2. Clone the repository to a local machine:
```bash
git clone https://github.com/skittree/university-api.git
```

3. (Recommended) Edit the `.env` file in the root directory to store your own configuration parameters for the API for safety reasons:

```dotenv
PORT={your_api_port}
POSTGRES_USER={your_db_username}
POSTGRES_PASSWORD={your_db_password}
POSTGRES_SERVER={your_db_server}
POSTGRES_PORT={your_db_port}
POSTGRES_DB={your_db_name}
```

4. Run the script `compose.sh` to install the requirements and build the necessary Docker containers, images and volumes. The database tables are automatically initialized upon launch:

```bash
docker compose -f "docker-compose.yml" up -d --build
```

## Usage

To launch the documentation on a local machine that is running the API on default port `8000`, you can use the following link: http://localhost:8000/docs:

![image](https://github.com/skittree/university-api/assets/32728173/f329fd51-edc9-4041-93eb-e17be0da02aa)

Similarly, using the default `.env` parameters, the DB connection link is `postgresql://localhost:5432/university`.
