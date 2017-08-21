# 小组成员

> Group SaGuaLiaZao 仨瓜俩枣小组
> 盛晓颖,左婧,肖飞,禚晨晨,樊文杰

# 把项目部署到vagrant虚拟机:
激活你的虚拟环境
``` bash
git clone http://se.jisuanke.com/code-game/Group1.git
cd Group1
chmod +x init.sh
./init.sh
```

# 运行程序
``` bash
Group1> python manage.py runserver
```

# 查看前后端文档
前端文档的快捷方式  Group1/frontend_doc.html
后端文档的快捷方式  Group1/backend_doc.html

# 常见问题
1.获取项目,SSH方法暂时链接不了,先使用HTTP方法
``` bash
git clone http://se.jisuanke.com/code-game/Group1.git
```
如果出现认证错误,在shell中输入
``` bash
export GIT_SSL_NO_VERIFY=1
```
or
``` bash
git config --global http.sslverify false
```
然后重新git clone即可

2.数据库doublegame已经存在
``` bash
mysql -uroot -pvagrant
drop database doublegame
create database doublegame default character set utf8 collate utf8_unicode_ci;
exit
```

# 组内约定
1.提交更改
``` bash
# 添加修改到提交列表
git add .
# 查看修改状态
git status
# 提交更改
git commit -m "这里是提交说明"
# 推送到gitlab
git push origin 分支名字
```

2.安装新插件
如果使用pip安装新的插件，  
安装完之后在项目文件夹（doublegame）中执行  
``` bash
  pip freeze > requirements.txt  
```
把你安装的插件写入到requirements.txt这个清单中  

如果使用npm安装新的插件,  
在安装的时候记得使用  
``` bash
npm install --save 插件名  
```
把你安装的插件写入到package.json这个清单中


3.静态资源放置
如果你在前端要新建一些静态文件(js\html\css\图片)  
如果和某一个vue组件有关的,放到frontend/src/assets里面,这里的文件会被webpack打包  
如果和vue组件无关的,放到frontend/static,这里的文件生成时会直接被复制


4.代码风格说明
基本使用Standard ESlint,仅将缩进设置为4空格  
所以有一些比较坑的东西  
不改正ESlint的所有错误的话 npm run dev不会正常运行

推荐在编译器安装pylint
要求更细,比如在函数前写一行注释,在函数第一行写doc...

5.在Vue(JavaScript/HTML/CSS)中
变量名/函数名使用小驼峰  
静态变量使用大写(加下划线还是破折号等遇到我再写)  
单文件组件的文件名使用大驼峰  
组件的'name'属性使用小写字母破折号(aaa-bbb)  
HTML/CSS使用小写字母破折号(aaa-bbb)  
类名使用大驼峰(MyClass)

``` bash
在操作符(+,-,=等等)前后要有空格
不能出现分号
function () 在'function'和'()'中间要有空格
除函数调用外出现()和{}前后一般要有空格
行尾不能有多余空格
文件末尾留一行空行
参数列表在','后面要有一个空格,例 function(a, b, c)
缩进要对齐
......
```


6.在Django(python)中
变量名/函数名使用小写字母下划线(aaa_bbb)  
静态变量使用大写下划线(AAA_BBB)  
类名使用大驼峰(MyClass)  
装完pylint就清楚了...

7.python和js的不同的包名规则
python中目录结构使用'.',类似java  
JS中目录结构使用'/'  
