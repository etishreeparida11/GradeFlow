
CREATE DATABASE IF NOT EXISTS StudentDB;
USE StudentDB;

CREATE TABLE IF NOT EXISTS Students (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(50) NOT NULL,
    marks DECIMAL(5,2) NOT NULL,
    department VARCHAR(50) NOT NULL
);

-- Calculate a student's grade
DROP FUNCTION IF EXISTS GetGrade;

DELIMITER //

CREATE FUNCTION GetGrade(marks DECIMAL(5,2))
RETURNS VARCHAR(10)
DETERMINISTIC
BEGIN
    IF marks >= 80 THEN
        RETURN 'A';
    ELSEIF marks >= 60 THEN
        RETURN 'B';
    ELSEIF marks >= 40 THEN
        RETURN 'C';
    ELSE
        RETURN 'Fail';
    END IF;
END //

DELIMITER ;

-- Add a new student
DROP PROCEDURE IF EXISTS AddStudent;

DELIMITER //

CREATE PROCEDURE AddStudent(
    IN p_id INT,
    IN p_name VARCHAR(50),
    IN p_marks DECIMAL(5,2),
    IN p_department VARCHAR(50)
)
BEGIN
    INSERT INTO Students (
        student_id,
        student_name,
        marks,
        department
    )
    VALUES (
        p_id,
        p_name,
        p_marks,
        p_department
    );
END //

DELIMITER ;

-- Add the original sample records only if their IDs do not exist
INSERT IGNORE INTO Students
    (student_id, student_name, marks, department)
VALUES
    (1, 'Rahul Sharma', 85, 'Computer Science'),
    (2, 'Priya Das', 72, 'Cloud Computing'),
    (3, 'Aman Verma', 45, 'Data Science'),
    (4, 'Neha Singh', 90, 'Cloud Computing'),
    (5, 'Ishita Rao', 66, 'Computer Science');
