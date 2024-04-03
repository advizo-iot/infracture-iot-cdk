CREATE EXTERNAL TABLE IF NOT EXISTS production_raw_iot_advizo.users (
  id VARCHAR(255),
  username VARCHAR(255),
  password VARCHAR(255),
  nombre VARCHAR(255)
)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ','
ESCAPED BY '\\'
COLLECTION ITEMS TERMINATED BY '|'
MAP KEYS TERMINATED BY ':'
STORED AS TEXTFILE
LOCATION 's3://advizo-iot-fire-resources/athenadb/input/production_raw_iot_advizo/users';