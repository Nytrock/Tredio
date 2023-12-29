<p align="center"><img src="Logo.png" alt="Logo" width="256"></p>

# Tredio

Tredio это площадка-агрегатор для поиска информации и оценки театров, постановок и актеров. Так же присутствуют возможность создания групп для совместного похода на постановку. 


# Сайт

Больше не хостируется по причине распада команды. Единственная возможность его опробовать - запустить на локальной машине, о чём ниже.

> Если вы столкнулись с какой-либо ошибкой, пожалуйста, создайте [issue](https://github.com/Nytrock/Tredio/issues).



# Инструкция по запуску на локальной машине

 - Клонировать репозиторий

	```shell
	git clone https://github.com/Nytrock/Tredio.git
	```

 - Установить зависимости с помощью requirements.txt или poetry
	```shell
	pip install -r requirements.txt
	```

 - Запустить сервер
	```shell
	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver
	```

 - Создать админку
	```shell
	python manage.py createsuperuser
	``` 

 - Зайти в админ панель, которая по умолчанию располагается по адресу `http://127.0.0.1:8000/admin/` 
 - Добавить категории отзывов и ранги
 

# Технические моменты

## Архитектура базы данных

![База данных](https://cdn.discordapp.com/attachments/968543211448594457/980101919601229864/models.png)

## Архитектура сайта

![База данных](https://cdn.discordapp.com/attachments/969630188155584512/980098403583271002/Untitled_Diagram.drawio.png)

# Команда

|[Артём](https://github.com/Jubastik)  |[Я](https://github.com/Nytrock)  | [Данил](https://github.com/PatriotRossii) |
|--|--|--|

