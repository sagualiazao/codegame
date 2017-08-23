touch import.sql
echo """
use doublegame;
delete from api_gamelevels;
load data local infile \"./levelinfo\" ignore into table doublegame.api_gamelevels FIELDS terminated by '$\n' LINES starting by '{\n' terminated by '}\n' (map_id, map, name, tips, codes, mode)
" > import.sql
mysql -h localhost -u root -pvagrant < ./import.sql
rm import.sql
echo 关卡信息已写入

