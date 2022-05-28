# Tredio

Tredio это площадка-агрегатор для поиска информации и оценки театров, постановок и актеров. Так же присутствуют возможность создания групп для совместного похода на постановку. 


# Сайт

Сайт - https://squid-app-536wx.ondigitalocean.app/

> Если вы столкнулись с какой либо ошибкой, пожалуйста сойзайте [issue](https://github.com/Jubastik/YlPlusProject/issues).
> 
> PS для ревьютеров. На сайте могут быть неожиданные ошибки. Если вы столкнулись с ними, попробуйте запустить сайт на локальной машине. Ну и конечно мы всегда рады вышим [issue](https://github.com/Jubastik/YlPlusProject/issues).



# Инструкция по запуску

 - Клонировать репозиторий

	```shell
	git clone https://github.com/Jubastik/YlPlusProject.git
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

|[Артём](https://github.com/Jubastik)  |[Сава](https://github.com/Nytrock)  | [Данил](https://github.com/PatriotRossii) |
|--|--|--|

