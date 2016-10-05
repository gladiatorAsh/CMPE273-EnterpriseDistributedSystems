Use cmpe273;
CREATE TABLE expenses (  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), email VARCHAR(30),category VARCHAR(20),description VARCHAR(50),link VARCHAR(50),
                       estimated_costs VARCHAR(50), submit_date DATE, status VARCHAR(50),decision_date DATE);
