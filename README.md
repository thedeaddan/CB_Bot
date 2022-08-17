# CB_Bot
Бот для отслеживания Евро и Доллара по ЦБ  
## Инструкция по использованию:
1. Проверьте, что у вас установлен Python 3.10+.
2. Форкните репозиторий, а затем склонируйте.<br>
3. Для работы с ботом необходимо установить пакеты с помощью:<br>
<code>pip install -r requirements.txt</code><br>
Либо установите пакеты: pyTelegramBotAPI, requests, bs4, lxml с помощью команды:<br>
<code>pip install _package_name_</code>
4. Создайте файл settings.py, в котором будет информация о вашем боте. Пример файла settings.py:<br>
<code>BOT_TOKEN = 'token'</code><br>
<code>BOT_NAME = '@bot_name'</code><br>
\* инструкция по созданию тг бота и получению токена по ссылке: https://clck.ru/dWnJq
5. Запустите файл bot.py.

## Список команд:  
- **/start** - начать общение с ботом  
![image](https://user-images.githubusercontent.com/40400854/185115820-0f5648d0-57c4-43b2-b403-436f538358d2.png)  
- **/go** - начать отслеживание  
![image](https://user-images.githubusercontent.com/40400854/185115909-b4295fb9-2502-44d7-bc08-fbfbca12486c.png)  
- **/info** - Получить сводку за последний день  
![image](https://user-images.githubusercontent.com/40400854/185116204-0daa6b68-4caa-4808-900b-dbfb3d77d670.png)  
- **/stop** - Отписаться от отслеживания   
![image](https://user-images.githubusercontent.com/40400854/185116292-392353e4-c425-4baa-addc-a08114ce83d1.png)  
##
За функцию запроса к серверам ЦБ спасибо [@alenapoliakova](https://github.com/alenapoliakova)

