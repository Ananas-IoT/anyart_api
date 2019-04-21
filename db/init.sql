CREATE USER 'anyart'@'localhost' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON anyart_db.* TO 'anyart'@'localhost';
FLUSH PRIVILEGES;