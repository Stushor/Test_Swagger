# Тестовое задание: Автоматизация API тестирования Swagger Petstore

## Общая информация

Этот проект представляет собой тестовую базу для функционального тестирования API сервиса [Swagger PetStore](https://petstore.swagger.io/v2). Он разработан на Python с использованием [pytest](https://docs.pytest.org/) и [requests](https://docs.python-requests.org/) для обеспечения масштабируемости тестов. Архитектура проекта позволяет легко добавлять новые тесты, избегая дублирования кода, за счёт использования централизованного API-клиента и общих фикстур.

## Как запускать тесты

### Необходимые компоненты:
- **Python 3.6+**
- **pip**
- **pytest 8.3.5**
- **requests 2.32.3**

### Установка зависимостей:
1. **Создайте и активируйте виртуальное окружение (рекомендуется):**
   - Для Linux/MacOS:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
   - Для Windows:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```

2. **Установите необходимые пакеты:**
   ```bash
   pip install -r requirements.txt.
   ```
   
### Запуск тестов:
1. Перейдите в корневую директорию проекта:
2. Убедитесь, что в ней находятся файлы api_client.py и config.ini, а также папка tests.
  - Запустите pytest:
  ```bash
  pytest
  ```
  - Для более подробного вывода используйте:
  ```bash
  pytest -v
  ```
  - Или запустите тесты для конкретного файла, например:
  ```bash
  pytest tests/test_pet.py
  ```

## Какие тесты выполняются
Проект включает тесты для проверки следующих сущностей и HTTP-методов API:

### 1. Pet (Питомцы):
- GET — Получение питомца по ID.
- POST — Создание питомца.
- PUT — Обновление данных питомца.
- DELETE — Удаление питомца.
- Параметризированные тесты для проверки корректного и некорректного ID.
  
### 2. User (Пользователи):
- POST — Создание пользователя.
- GET — Получение данных пользователя.
- PUT — Обновление данных пользователя.
- DELETE — Удаление пользователя.
- Параметризированные тесты для создания пользователей с разными наборами входных параметров.

### 3. Store (Заказы и Инвентарь):
- GET — Получение инвентаря и получение заказа по ID.
- POST — Размещение заказа.
- DELETE — Удаление заказа.
- Проверка метода PUT для обновления заказа (ожидается, что обновление не поддерживается, код 404 или 405).
- Параметризированные тесты для размещения заказов с различными входными данными.

## Информация по каждому файлу
### api_client.py
**Модуль, содержащий класс APIClient, который инкапсулирует вызовы API (GET, POST, PUT, DELETE).**
Этот файл реализует методы для формирования URL запроса и отправки HTTP-запросов через библиотеку requests. Он обеспечивает централизованное управление вызовами API, что помогает избежать дублирования кода в тестах.

### config.ini
**Файл конфигурации.**
Содержит секцию [api] с настройками, такими как базовый URL API:
```ini
[api]
base_url = https://petstore.swagger.io/v2
```
Используется для централизованного управления параметрами тестового окружения.

### tests/conftest.py
**Файл с общими фикстурами и настройками для всех тестов.**
Здесь определяются:
- Фикстура api_client, создающая экземпляр класса APIClient.
- Фикстуры для создания сущностей: питомца (created_pet), пользователя (created_user) и заказа (created_order).
- Добавление родительской директории в sys.path для корректного импорта модуля api_client.py.

### tests/test_pet.py
**Тесты для проверки функциональности API, связанных с питомцами.**
Содержит тесты для:
- Получения питомца по ID.
- Проверки статуса ответа для корректного и некорректного ID (с использованием параметризации).
- Обновления данных питомца.
- Удаления питомца и проверки его удаления.

### tests/test_user.py
**Тесты для проверки функциональности API, связанных с пользователями.**
Реализует тесты для:
- Создания пользователя и проверки его создания через GET-запрос.
- Обновления данных пользователя.
- Удаления пользователя и проверки удаления.
- Параметризированного теста для создания пользователей с разными наборами входных параметров.

### tests/test_store.py
**Тесты для проверки функциональности API, связанных с заказами и инвентарем.**
Включает тесты для:
- Получения инвентаря.
- Размещения заказа и проверки корректности созданного заказа.
- Получения заказа по ID.
- Удаления заказа и проверки удаления.
- Проверки, что обновление заказа методом PUT не поддерживается.
- Параметризированного теста для размещения заказов с различными параметрами.

Этот проект демонстрирует модульный и масштабируемый подход к автоматизированному тестированию API, обеспечивая простоту поддержки и расширения тестовой базы по мере роста проекта.
