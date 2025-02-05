create table users (
	id SERIAL PRIMARY KEY,
	username VARCHAR(50),
	email VARCHAR(50),
	password_hash VARCHAR(150),
	ip_address VARCHAR(20),
	created_at DATE,
	last_login_time VARCHAR(50),
	country_code VARCHAR(50),
	phone VARCHAR(50)
);

create table customers (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    address TEXT,
    contact_phone VARCHAR(20),
    date_of_birth DATE
);