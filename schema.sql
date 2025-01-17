
create table IF NOT exists score (
  `student_id` integer not null,
  `test_number_id` integer not null,
  `curriculum_id` integer not null,
  `point` integer not null,
  foreign key(student_id) references student(student_id)
  foreign key(test_number_id) references test_number(test_number_id)
  foreign key(curriculum_id) references curriculum(curriculum_id)
  Primary key(student_id, test_number_id, curriculum_id)
);

create table IF NOT exists student (
  `student_id` integer not null Primary key,
  `name` integer not null
);

create table IF NOT exists test_number (
  `test_number_id` integer not null Primary key,
  `name` integer not null
);

create table IF NOT exists curriculum (
  `curriculum_id` integer not null Primary key,
  `name` integer not null
);


select t.name, s.test_id, s.html_score, s.css_score, s.js_score, s.python_score, s.java_score
from score as s
join test_number as t
on s.test_id = t.test_id
order by t.test_id asc;