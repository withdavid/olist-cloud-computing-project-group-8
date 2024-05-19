UPDATE mysql.user SET Host='%' WHERE User='olist_myuser';
FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_category_name VARCHAR(50),
    product_name_length INT,
    product_description_length INT,
    product_photos_qty INT,
    product_weight_g INT,
    product_length_cm INT,
    product_height_cm INT,
    product_width_cm INT,
    price DECIMAL(10,2) NOT NULL
);