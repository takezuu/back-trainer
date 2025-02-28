create table users (
	id SERIAL PRIMARY KEY,
	email VARCHAR(50),
	phone VARCHAR(50),
	full_name VARCHAR(100),
	password VARCHAR(150),
	ip_address VARCHAR(20),
	last_login_time TIMESTAMP,
	country_code VARCHAR(50),
	balance INT,
	can_delete boolean,
	UNIQUE (email, phone)
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
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