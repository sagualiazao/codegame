# git clone http://se.jisuanke.com/code-game/Group1.git


# pwd: Group1/
# 创建数据库
touch init.sql
echo "drop database if exists buildtest;" > init.sql
echo "create database buildtest default character set utf8 collate utf8_unicode_ci;" >> init.sql
mysql -h localhost -u root -pvagrant < ./init.sql
rm init.sql
echo 数据库已创建


# pwd: Group1/
# 生成数据模型
python manage.py makemigrations
python manage.py migrate
echo 数据模型已创建


# pwd: Group1/
# 写入关卡信息
mysql -h localhost -u root -pvagrant < ./import.sql
echo 关卡信息已写入


# pwd: Group1/
# 安装python依赖
pip install -r requirements.txt 
echo python依赖已安装


# pwd: Group1/
# 安装js依赖
cd frontend
npm install
echo JavaScript依赖已安装


# pwd: Group1/frontend
# 构建前端资源
npm run build
echo 前端资源构建完成


# pwd: Group1/
# 链接静态资源
cd ../api
ln -s ../frontend/dist/ templates
ln -s ../frontend/dist/static/ static
echo 静态资源已连接


# pwd: Group1/api
# 构建文档
cd ../docs/django/
mkdir source/_static
make clean
sphinx-build -b html source build
make html
echo 后端文档构建完成

# pwd: Group1/docs/django
cd ../../
echo 现在你可以使用
echo 'python manage.py runserver'
echo 来运行项目
echo 如果你使用的是vagrant虚拟机,请使用
echo 'python manage.py runserver 0:8000'
echo 后端文档位于 docs/django/build/html/index.html
echo =============================================
