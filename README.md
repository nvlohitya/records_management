## Records Management Web App

### Clone
```bash
git clone git@github.com:nvlohitya/records_management.git
cd records_management
```

### Install Dependencies

#### Flask
```bash
python3 -m venv venv # use "py -m venv venv" for windows
./venv/Scripts/activate
```

### Start Servers

#### Flask
Open new terminal
```bash
flask run
```

### Creating the database
```bash
#### Install DB Browser GUI for creating a database and create 3 tables :- Students , Courses and Enrollments
#### Students :- Columns should be student_id(Primary Key) , roll_number , first_name , last_name
#### Courses :- Columns should be course_id(Primary Key) , course_code , course_name , course_description
#### Enrollments :- Columns should be enrollment_id(Primary Key) , estudent_id(Foreign Key student.student_id) , ecourse_id(Foreign Key course.course_id)
```



