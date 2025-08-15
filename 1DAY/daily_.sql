create database life_logger_db;
use life_logger_db;

create table daily_logs(
	log_id integer primary key auto_increment,
    log_date date not null unique,
    sleep_start_time datetime,
    sleep_end_time datetime,
    did_workout boolean not null default false
    );
    
create table exercises(
	exercise_id integer primary key auto_increment,
    exercise_name varchar(100) not null unique,
    targer_part varchar(50)
    );
    
create table exercise_logs(
	set_id integer primary key auto_increment,
    log_id integer not null,
    exercise_id integer not null,
    set_number integer not null,
    weight decimal(5,2) not null,
    reps int not null,
    foreign key (log_id) references daily_logs(log_id),
    foreign key (exercise_id) references exercise(exercises_id)
    );

create table expense_categories(
	category_id integer primary key auto_increment,
    category_name varchar(50) not null unique
    );
    
create table expense_records(
	expense_id int primary key auto_increment,
    log_id int not null,
    category_id int not null,
    amount int not null,
    description varchar(255),
    foreign key (log_id) references daily_logs(log_id),
    foreign key (category_id) references expense_categories(category_id)
    );
    
insert into exercise (exercise_name, target_part) values ('bench_press', 'chest');
insert into exercise (exercise_name, target_part) values ('cable_cross_over', 'chest');
insert into exercise (exercise_name, target_part) values ('incline_bench_press', 'chest');
insert into exercise (exercise_name, target_part) values ('dumbbell_curl', 'biceps');
insert into exercise (exercise_name, target_part) values ('hammer_curl', 'biceps');
insert into exercise (exercise_name, target_part) values ('barbell_curl', 'biceps');
insert into exercise (exercise_name, target_part) values ('pull_up', 'back');
insert into exercise (exercise_name, target_part) values ('barbell_low', 'back');
insert into exercise (exercise_name, target_part) values ('dumbbell_low', 'back');
insert into exercise (exercise_name, target_part) values ('sitted_low', 'back');
insert into exercise (exercise_name, target_part) values ('triceps_extension', 'triceps');
insert into exercise (exercise_name, target_part) values ('dumbbell_overhead_extension', 'triceps');
insert into exercise (exercise_name, target_part) values ('cable_push_down', 'triceps');
insert into exercise (exercise_name, target_part) values ('side_lateral_raise', 'shoulder');
insert into exercise (exercise_name, target_part) values ('shoulder_press', 'shoulder');
insert into exercise (exercise_name, target_part) values ('barbell_shoulder_press', 'shoulder');
insert into exercise (exercise_name, target_part) values ('leg_extension', 'leg');
insert into exercise (exercise_name, target_part) values ('leg_press', 'leg');
insert into exercise (exercise_name, target_part) values ('squat', 'leg');

insert into expense_categories (category_name) values ('food');
insert into expense_categories (category_name) values ('fixd');
insert into expense_categories (category_name) values ('hobby');
insert into expense_categories (category_name) values ('savings');

select * from exercise;
select * from expense_categories;

INSERT INTO daily_logs (log_date, sleep_start_time, sleep_end_time, did_workout)
VALUES ('2025-08-13', '2025-08-13 01:00:00', '2025-08-13 08:30:00', TRUE);

INSERT INTO exercise_logs (log_id, exercise_id, set_number, weight, reps) VALUES (1, 12, 3, 8, 12); -- side_lateral_raise
INSERT INTO exercise_logs (log_id, exercise_id, set_number, weight, reps) VALUES (1, 13, 3, 14, 12);  -- shoulder_press
INSERT INTO exercise_logs (log_id, exercise_id, set_number, weight, reps) VALUES (1, 14, 4, 30, 8);  -- barebell_shoulder_press
INSERT INTO exercise_logs (log_id, exercise_id, set_number, weight, reps) VALUES (1, 15, 3, 28, 12); -- leg_extension
INSERT INTO exercise_logs (log_id, exercise_id, set_number, weight, reps) VALUES (1, 16, 3, 100, 12);  -- leg_press
INSERT INTO exercise_logs (log_id, exercise_id, set_number, weight, reps) VALUES (1, 17, 4, 60, 8); -- sqaut


INSERT INTO expense_records (log_id, category_id, amount, description) VALUES (1, 1, 800, 'lunch'); -- 식비
INSERT INTO expense_records (log_id, category_id, amount, description) VALUES (1, 2, 3510, 'electricity bill');     -- 고정
INSERT INTO expense_records (log_id, category_id, amount, description) VALUES (1, 1, 650, 'beer');  -- 식비

select * from exercise_logs;

update exercise set exercise_name = 'barbell_row' where exercise_name = 'barbell_low';
update exercise set exercise_name = 'dumbbell_row' where exercise_name = 'dumbbell_low';
update exercise set exercise_name = 'sitted_row' where exercise_name = 'sitted_low';

select * from exercise;

select sum(amount) as '총지출액' from expense_records where log_id = 1;

SELECT
    e.exercise_name AS '운동 이름',
    COUNT(el.set_id) AS '총 세트 수'
FROM exercise_logs AS el
JOIN exercises AS e ON el.exercise_id = e.exercise_id
WHERE el.log_id = 1
GROUP BY e.exercise_name;

	