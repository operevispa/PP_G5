# Проектный практикум, группа 5
## Проект: Помощник для студента
___

### Начало работы
Помощник работает в виде веб-приложение по ссылке http://158.160.48.28:8501
Для запуска проекта локально необходимо скачать исходный код проекта ppmain.py и настроить локальную среду разработки. 
Рекомендуем установить виртуальное окружениие. Это можно сделать следующей командой:
```bash
python3 -m venv namedir
```
После установки виртуального окружения необходимо ее активировать
- команда для linux:
```bash
source namedir/bin/activate
```
- команда для windows:
```
.\scripts\activate.ps1
```
И далее установить в активированную виртуальную среду список необходимых библиотек для работы приложения. 
Все необходимые бибилиотеки перечислены в requirements.txt. Для массовой установки бибилиотек достаточно использовать команду:
```bash
pip install -r requirements.txt
```
В проекте используется две предобученные модели:
- хххххх - для генерации саммари-информации по большому объему загруженных в нее данных
- хххххх - для получения быстрых ответов на вопросы по загруженному в модель контенту

### Варианты использования приложения
Приложение помогает с минимальными затратами времени получить необходимую информацию из больших объемов текста. Так, саммари позволяет вместо 10минут потратить менее 1 минуты на получение основного смысла статьи или абзаца из книги. При появлении конкретных вопросов к тексту, нет необходимости использовать контекстный поиск - вместо этого можно задать интересующий вопрос и если ответ на этот вопрос в том или ином виде представлен в загруженных данных - получить ответ.
Получив саммари и ответы, пользователь может узнать, например, имеется ли необходимая ему информация в статье и стоит ли потратить больше времени на ее детальное изучение. 

### Команда проекта:
- Игорь Ерошин, менеджер проекта
- Татьяна Меркурьева, аналитик данных
- Евгений Брылин, Инженер по машинному обучению
- Олег Перевиспа, Full Stack-разработчик
- Вадим Монахов, Тестировщик-QA инженер
- Клим Колчин, Документалист/технический писатель

### Лицензия
Приложение распостраняется по лицензии хххх