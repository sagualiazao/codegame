# 安装必要的软件包等
pip install -r requirements.txt
echo python依赖已安装

# 创建数据库
touch init.sql
echo """
drop database if exists doublegame;
create database doublegame default character set utf8 collate utf8_unicode_ci;
" > init.sql
mysql -h localhost -u root -pvagrant < ./init.sql
rm init.sql
echo 数据库已创建

# 建立数据模型
python manage.py makemigrations
python manage.py migrate
echo 数据模型已创建

# 写入关卡信息
touch import.sql
echo """
use doublegame;
delete from api_gamelevels;
load data local infile \"./levelinfo\" ignore into table doublegame.api_gamelevels FIELDS terminated by '$\n' LINES starting by '{\n' terminated by '}\n' (map_id, map, name, tips, codes, mode)
" > import.sql
mysql -h localhost -u root -pvagrant < ./import.sql
rm import.sql
echo 关卡信息已写入

# 安装js依赖
cd frontend
npm install
echo JavaScript依赖已安装

# 构建前端资源
npm run build
echo 前端资源构建完成

# 链接静态资源
cd ../api
ln -s ../frontend/dist templates
ln -s ../frontend/dist/static static
echo 静态资源已连接

#前端文档生成
cd ../frontend/src/components
for name in *.vue;do cp $name ${name%.vue}.js;done
cd ../../
sudo npm -g install yuidocjs
yuidoc .
cd ./src/components
rm *.js

# 后端文档生成
cd ../../../docs/django
mkdir source/_static
make clean
sphinx-build -b html source build
make html
echo 后端文档构建完成

# 生成前端文档快捷方式
cd ../../
ln -s ./frontend/out/index.html frontend_doc.html

# 生成后端文档快捷方式
ln -s ./docs/django/build/html/index.html backend_doc.html

# 部署完成提示信息
echo 现在你可以使用
echo 'python manage.py runserver'
echo 来运行项目
echo 如果你使用的是vagrant虚拟机,请使用
echo 'python manage.py runserver 0:8000'
echo 前端文档的快捷方式  Group1/frontend_doc.html
echo 后端文档的快捷方式  Group1/backend_doc.html
echo =============================================
