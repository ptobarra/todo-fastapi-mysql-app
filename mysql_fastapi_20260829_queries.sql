SELECT * FROM TODOS;

SELECT * FROM USERS;

ALTER TABLE users
ADD COLUMN phone_number VARCHAR(255) NULL;

ALTER TABLE users DROP COLUMN phone_number;

DELETE FROM users WHERE username = 'ptobarra';
