create table users (
	id SERIAL PRIMARY KEY,
	username VARCHAR(50),
	email VARCHAR(50),
	password_hash VARCHAR(150),
	ip_address VARCHAR(20),
	created_at DATE,
	last_login_time VARCHAR(50),
	country_code VARCHAR(50),
	phone VARCHAR(50),
	UNIQUE (email, phone)
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


CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    items_ids INT[] NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    discount FLOAT8 DEFAULT 0.0,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    delivery_address VARCHAR(200)
);

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL,
    category VARCHAR(100),
    item_color VARCHAR(20),
    rating INT DEFAULT NULL
);