
CREATE DATABASE IF NOT EXISTS StudentDB;
USE StudentDB;

CREATE TABLE IF NOT EXISTS Students (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    marks DECIMAL(5,2) NOT NULL,
    department VARCHAR(100) NOT NULL,
    CHECK (marks >= 0 AND marks <= 100)
);

DROP FUNCTION IF EXISTS GetGrade;

DELIMITER $$

CREATE FUNCTION GetGrade(p_marks DECIMAL(5,2))
RETURNS VARCHAR(10)
DETERMINISTIC
NO SQL
BEGIN
    IF p_marks >= 80 THEN
        RETURN 'A';
    ELSEIF p_marks >= 60 THEN
        RETURN 'B';
    ELSEIF p_marks >= 40 THEN
        RETURN 'C';
    ELSE
        RETURN 'Fail';
    END IF;
END$$

DELIMITER ;

DROP PROCEDURE IF EXISTS AddStudent;

DELIMITER $$

CREATE PROCEDURE AddStudent(
    IN p_id INT,
    IN p_name VARCHAR(100),
    IN p_marks DECIMAL(5,2),
    IN p_department VARCHAR(100)
)
BEGIN
    IF p_marks < 0 OR p_marks > 100 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Marks must be between 0 and 100';
    END IF;

    INSERT INTO Students (
        student_id, student_name, marks, department
    )
    VALUES (
        p_id, p_name, p_marks, p_department
    );
END$$

DELIMITER ;
