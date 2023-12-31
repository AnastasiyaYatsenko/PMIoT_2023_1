# PMIoT_2023_1
Repository for PMIoT project of the group 2023-1 (Arkhypov, Kryvous, Karnaukh, Yatsenko)

# Швидкий запуск
1. Завантажуємо усі файли проекту з віддаленого Git репозиторію.
2. Встановлюємо Python останньої версії (>3.12). Офіційний сайт Python: https://www.python.org/downloads/
3. Створюємо віртуальне середовище:
   - відкриваємо термінал, переходимо до робочої папки
   - вводимо в термінал в залежності від ОС:
     
     **Linux**
     
     ```
     sudo apt-get install python3-venv
     python3 -m venv .venv
     source .venv/bin/activate
     ```
  
     **macOS**
     
     ```
     python3 -m venv .venv
     source .venv/bin/activate}
     ```
      
     **Windows**
  
     ```
     py -3 -m venv .venv
     .venv\scripts\activate
     ```
     
4. Оновлюємо менеджер пакетів:
   
   ```
   python -m pip install --upgrade pip
   ```
   
5. Встановлюємо Django:
 
   ```
   python -m pip install django
   ```
   
6. Встановлюємо пакет pytz для роботи з таймзонами:
 
   ```
   pip install pytz
   ```
   
7. Встановлюємо пакет pandas для роботи з датасетом:
 
   ```
   pip install pandas
   ```
      
8. Встановлюємо пакет Pillow для роботи з картинками:
 
   ```
   pip install Pillow
   ```
      
9. Встановлюємо пакет scikit-learn для роботи функцій прогнозування:
 
   ```
   pip install scikit-learn
   ```
   
10. Запускаємо локальний сервер:
   
   ```
   python manage.py runserver
   ```

# Встановлення серверу
Встановлення серверу складається з наступних компонентів:
- налаштування файлів конфігурацій мікро-серверу uWSGI для запуску Django-застосунку
- налаштування утиліти Supervisor, яка запускає uWSGI при старті системи
- налаштування NGINX - потужного проксі-серверу до uWSGI

# WSGI. 
Веб сервер приймає та обслуговує запити. Він може віддавати файли (HTML, зображення, CSS, і т.д.) безпосередньо зі своєї файлової системи. Однак він не може напряму працювати з Django застосуванням. Необхідний інтерфейс, який буде запускати Django застосування, передавати йому запити від веб клієнта, наприклад браузера, і повертати відповіді.
Для цього був розроблений Web Server Gateway Interface (WSGI) - стандарт взаємодії Python програм і веб-сервера. uWSGI є однією з реалізацій WSGI. Необхідно налаштувати uWSGI для створення Unix-сокету та взаємодії з веб-сервером за допомогою протоколу WSGI.
Встановити uWSGI для Python можна, якщо активувати віртуальне середовище, та виконати команду:
```
pip install uwsgi
```

Далі необхідно створити новий файл uwsgi.ini поруч із manage.py з наступним змістом:

   ```
   [uwsgi]
   
   chdir = <шлях до папки з проєктом>/pmiot_site
   
   module=project.wsgi
   
   socket = 127.0.0.1:8080
   
   chmod-socket=666
   
   home=<шлях до папки з проєктом>/pmiot_env
   
   req-logger = file:/var/log/uwsgi/req.log
   
   logger = file:/var/log/uwsgi/err.log
   
   static-map = /static=<шлях до папки з проєктом>/pmiot_site/pmiot/static
   ```

- chdir використовується для позначення каталогу проекту;
- module — Django wsgi файл;
- socket — вказує на адресу для підключення сокету. Якщо перейти за цією адресою у браузері, то користувач нічого не побачить, оскільки браузер використовує протокол http, а не uWSGI;
- chmod-socket — визначає права доступу до файлу сокета;
- home вказує на віртуальне оточення для вашого проекту.

# Система Supervisor. 
Supervisor ‒ це утиліта керування процесами в операційній системі. Нею можна скористатися, якщо є програми, які потребують перезапуску за певними правилами.  Таким чином не потрібно буде писати підсистему управління (rc-скрипти, систему моніторингу та перезапуску) для таких програм.
Supervisor запускає процеси як свої підпроцеси, тому він має над ними повний контроль і знає їх точний стан.
supervisorctl надає системний контроль, а також веб-інтерфейси для моніторингу та керування процесами. Користувач може бачити стан програм та виконувати дії над ними (start, stop, restart).
Можна групувати програми і здійснювати над ними спільні дії (наприклад, перезавантаження всіх програм). Також є можливість вказувати пріоритет для кожної програми, тим самим організовуючи порядок перезапуску.
Ця утиліта написана на Python, працює на Linux, Mac OS X, Solaris і FreeBSD.
Необхідно додати запуск Django проекту до Supervisor. Якщо утілита ще не встановлена, виконайте:
```
sudo apt-get install supervisor
```
Далі додайте файл djangoproject.conf до каталогу /etc/supervisor/conf.d:
```
[program:djangoproject]

directory=<шлях до папки з проєктом>/pmiot_site

command=<шлях до папки з проєктом>/pmiot_env/bin/uwsgi --ini uwsgi.ini 

stdout_logfile=<шлях до папки з проєктом>/logs/supervisor.log
```
 
- directory вказує на головну директорію вашого проекту;
- command визначає безпосередньо команду яка буде виконуватися та відстежуватися;
- stdout_logfile вказує на файл, куди записується уся інформація щодо роботи вашої програми.

Перейдіть до каталогу  django-project та виконайте:
```
mkdir logs
```
Виконайте команду для оновлення конфігурацій:
```
sudo supervisorctl reread
```
У терміналі повинні побачити наступне:
```
djangoproject: available
```
Далі потрібно виконати команду для перезапуску утиліти:
```
sudo supervisorctl reload
```
Виконайте команду:
```
sudo supervisorctl
```
Якщо все виконано правильно, ви побачите приблизно наступне:

djangoproject                    RUNNING    pid 13390, uptime 0:00:07

Якщо замість цього и бачите помилку або статус FATAL, це означає, що конфігурація виконана неправильно. Переглянути деталі можна в файлі /home/user/django-project/logs.
 

# NGINX
NGINX – програмне забезпечення, написане для UNIX-систем. Основне призначення – самостійний HTTP-сервер, або, як його використовують частіше, фронтенд для високонавантажених проектів. Можливе використання NGINX як SMTP/IMAP/POP3-сервера, а також зворотного TCP проксі-сервера.
Для встановлення:
```
sudo apt-get install nginx
```
Для запуску(start), зупинки(stop) або перегляду стану(status) ngninx служби виконайте:
```
sudo service nginx <action>
```
Для того, щоб nginx застосував нові налаштування, виконайте:
```
sudo service nginx reload
```
Для перевірки правильності конфігурацій, існує команда:
```
sudo nginx -t
```
Перевірте статус програми, та запустіть якщо необхідно. До каталогу /etc/nginx/sites-available додайте файл  djangoproject.conf:
```
upstream django {

    server 127.0.0.1:8080;
    
}

server {

    listen      9000;
    
    location / {
    
        uwsgi_pass  django;
        
        include     uwsgi_params;
        
    }
    
}
```
В даному файлі конфігурацій директива upstream описує сервер, що слухає на UNIX-сокеті локально за портом 8080 (зпівпадає з параметром socket у файлі uwsgi.ini). Server задає адресу та інші параметри серверу. Директива listen відповідає за порт, за яким сайт буде доступним у браузері, location вказує куди повинен бути перенаправлений запит для оброблення. Таких директив може бути декілька, URL можуть бути задані регулярними виразами. В нашому випадку достатньо «/».
Перейдіть до /etc/nginx/sites-enabled та створіть посилання на щойно створений файл:
```
sudo ln -s /etc/nginx/sites-available/djangoproject.conf ./djangoproject.conf
```
Також у файлі /etc/hosts необхідно відредагувати рядок із локальною адресою та додати туди назву сайту за вашим бажанням, наприклад:
```
127.0.0.1    localhost djangoproject
```
Необхідно перезапустити nginx для застосування нових конфігурацій. Якщо налаштування були виконані правильно, то після переходу за адресою http://djangoproject:9000/ у браузері повинен відобразитися ваш проект.


# MQTT
MQTT — спрощений мережевий протокол, що працює на TCP/IP. Використовується для обміну повідомленнями між пристроями за принципом видавець-підписник.
Для встановлення:
1. Створити віртуальну машину з ОС Ubuntu
2. Встановити пакунок mosquitto
3. За допомогою команди mosquitto_passwd створити файл паролів у /etc/mosquitto/passwd і додати у файл конфігурацій рядок 
```
password_file /etc/mosquitto/passwd
```
4. Виконати команду systemctl restart mosquitto
5. Переконатися, що сервіс запущено: systemctl status mosquitto
Якщо все працює коректно, статус повинен бути active (running)

# MongoDB

Основні пункти для підготовки MongoDB:

**Linux**

- Встановлюємо пакет djongo:
   ```
   pip install djongo
   ```
- Встановлюємо пакет pymongo (конкретної версії):
   ```
   pip install pymongo==3.12.3
   ```
- Встановлюємо пакет mongodb-clients:
   ```
   sudo apt install mongodb-clients
   ```
- Встановлюємо пакет mongodb-server-core:
   ```
   sudo apt install mongodb-server-core
   ```

**Windows**

- Встановлюємо пакет djongo:
   ```
   pip install djongo --user
   ```
- Встановлюємо пакет pymongo (конкретної версії):
   ```
   pip install pymongo==3.12.3 --user
- Встановлюємо пакет mongodb з офіційного сайту: https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.4-signed.msi
- Встановлюємо пакет mongosh з офіційного сайту: https://downloads.mongodb.com/compass/mongosh-2.1.1-x64.msi
- Встановлюємо пакет mongocli з офіційного сайту: https://fastdl.mongodb.org/mongocli/mongocli_1.31.0_windows_x86_64.msi
- Встановлюємо пакет mongodb-dataset-tools з офіційного сайту: https://fastdl.mongodb.org/tools/db/mongodb-database-tools-windows-x86_64-100.9.4.msi
   
# MongoDB backup

У папці data_backup знаходяться початкові дані для бази даних (4 сенсори та декілька записів у архіві).
Вона була створена за допомогою спеціальної команди:
```
mongodump --out data_backup/
```
Разово на початку роботи із MongoDB для витягання цих даних або повному перезапису даних у папці data до початкових необхідно викликати спеціальну команду:

**Linux**

```
mongorestore --drop --dir data_backup
```

**Windows**

Та ж сама команда, але необхідно вказувати повний шлях до mongorestore:
```
"C:\...\mongorestore" --drop --dir data_backup
```
