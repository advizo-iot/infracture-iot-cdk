CREATE EXTERNAL TABLE IF NOT EXISTS production_raw_iot_advizo.map_factory (
  dni VARCHAR(255),
  map_id VARCHAR(255),
  url_map VARCHAR(255),
  coordenates VARCHAR(255)
)
ROW FORMAT DELIMITED 
FIELDS TERMINATED BY ','
ESCAPED BY '\\'
COLLECTION ITEMS TERMINATED BY '|'
MAP KEYS TERMINATED BY ':'
STORED AS TEXTFILE
LOCATION 's3://advizo-iot-fire-resources/athenadb/input/production_raw_iot_advizo/map_factory';