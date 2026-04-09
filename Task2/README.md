# Автоматизация тестов Task2

## Установка зависимостей

1. Установить Python 3.12+  
2. Создать виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
3. Установить необходимые пакеты:
       ```bash
        pip install -r requirements.txt
   
   В requirements.txt должны быть:
    ```bash
     requests
     pytest



### Запуск тестов

 1. Перейти в директорию с тестами:
    ```bash
     cd Task2
 2. Запустить все тесты:
    ```bash
     pytest test_avito_api.py -v
 3. Для генерации отчёта Allure (если установлен Allure):
     ```bash
      pytest --alluredir=allure-results
      allure serve allure-results


#### Файлы

     test_avito_api.py — автоматизированные тесты
     TESTCASES.md — описание всех тест-кейсов
     BUGS.md — зарегистрированные дефекты
