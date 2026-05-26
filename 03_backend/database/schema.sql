CREATE DATABASE IF NOT EXISTS hbdvap_system
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE hbdvap_system;

DROP TABLE IF EXISTS realtime_statistics;
DROP TABLE IF EXISTS prediction_records;
DROP TABLE IF EXISTS hotel_bookings;

CREATE TABLE hotel_bookings (
  id INT PRIMARY KEY AUTO_INCREMENT,
  hotel VARCHAR(50) NOT NULL,
  is_canceled INT,
  lead_time INT,
  arrival_date_year INT,
  arrival_date_month VARCHAR(20),
  arrival_date_week_number INT,
  arrival_date_day_of_month INT,
  stays_in_weekend_nights INT,
  stays_in_week_nights INT,
  adults INT,
  children DOUBLE,
  babies INT,
  meal VARCHAR(20),
  country VARCHAR(20),
  market_segment VARCHAR(50),
  distribution_channel VARCHAR(50),
  is_repeated_guest INT,
  previous_cancellations INT,
  previous_bookings_not_canceled INT,
  reserved_room_type VARCHAR(10),
  assigned_room_type VARCHAR(10),
  booking_changes INT,
  deposit_type VARCHAR(50),
  agent DOUBLE,
  company DOUBLE,
  days_in_waiting_list INT,
  customer_type VARCHAR(50),
  adr DOUBLE,
  required_car_parking_spaces INT,
  total_of_special_requests INT,
  reservation_status VARCHAR(50),
  reservation_status_date DATE,
  INDEX idx_hotel (hotel),
  INDEX idx_country (country),
  INDEX idx_customer_type (customer_type),
  INDEX idx_arrival_date_month (arrival_date_month)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE prediction_records (
  id INT PRIMARY KEY AUTO_INCREMENT,
  input_json JSON NOT NULL,
  is_canceled_pred INT NOT NULL,
  cancel_probability DOUBLE NOT NULL,
  risk_level VARCHAR(20) NOT NULL,
  suggestion VARCHAR(255) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_risk_level (risk_level),
  INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE realtime_statistics (
  id INT PRIMARY KEY AUTO_INCREMENT,
  stat_name VARCHAR(100) NOT NULL,
  stat_value DOUBLE NOT NULL,
  stat_dimension VARCHAR(100),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_stat_name (stat_name),
  INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
