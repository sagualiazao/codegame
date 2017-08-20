-- id, map, name, tips, codes, mode
-- mysql -h localhost -u root -pvagrant < ./import.sql 
-- ================================

use doublegame;
delete from api_gamelevels;
load data local infile "./levelinfo" ignore into table doublegame.api_gamelevels FIELDS terminated by '$\n' LINES starting by '{\n' terminated by '}\n' (map_id, map, name, tips, codes, mode)


