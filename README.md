# kafkey

kafka + key : kafka的监控管理工具


## 程序目录简介
* requirements.txt 程序依赖包列表
* manage.py 程序入口
* tests 测试类目录
* app 所有非测试程序存放目录


## 部署

* 激活虚拟环境

	```
	source ./venv/bin/activate
	```

* 安装虚拟环境依赖包

	```
	pip install -r requirements.txt
	
	# 如果没有requirements.txt, 可以在运行程序的主机上直接运行如下命令生成该文件
	(venv) $ pip freeze >requirements.txt
	```

* 初始化数据库

	```
	python manage.py initdb
	```

* 启动程序

	```
	python manage.py runserver --host 0.0.0.0
	
	# 查看帮助
	python manage.py runserver --help 
	```
	
* **关于migrate操作(此处暂时忽略)**

	* 创建数据迁移仓库


		```
		python manage.py db init
		```
	
	* 创建自动迁移脚本
	
		```
		python manage.py db migrate -m "initial migration"
		```
	
	* 应用迁移脚本到数据库中
	
		```
		python manage.py db upgrade
		```
     
   





