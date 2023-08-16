<p align="center">
<a href="https://ibb.co/gv0Dm98"><img src="https://i.ibb.co/JxYzmtT/kindpng-1795925-1.png" alt="kindpng-1795925-1" border="0"></a></p>

# Simple CDN server
<p align="center">
    <a href="https://codecov.io/gh/AndrewSergienko/simple-cdn-server" >
     <img src="https://codecov.io/gh/AndrewSergienko/simple-cdn-server/branch/master/graph/badge.svg?token=PHAIHK4J5U"/>
    </a>
    <img src="https://img.shields.io/badge/python-3.10-blue?logo=python" alt="Python Version">
    <a href="https://github.com/AndrewSergienko/simple-cdn-server/actions">
        <img src="https://img.shields.io/badge/tests-passed-green?logo=github" alt="Actions">
    </a>
    <a href=https://results.pre-commit.ci/latest/github/AndrewSergienko/simple-cdn-server/master>
        <img src=https://results.pre-commit.ci/badge/github/AndrewSergienko/simple-cdn-server/master.svg>
    </a>
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code_style-black-black" alt="black"></a>
</p>

## Про проект
Сервіс - хмарне сховище файлів. Надає можливість зберігати файли, які завантажаються
по посиланню. Після завантаження файлу проводить його реплікацію на інші вказані сервери.

## Як працює сервіс
На момент публікації записки, запущені 4 сервери:
<img src="https://i.ibb.co/RDB2mq1/2023-08-15-11-30-27.png" alt="2023-08-15-11-30-27" border="0">

Три файлові серери в різних локаціях: Франкфурт, Нью-Йорк, Сінгапур, та один головний сервер у Франкфурті.

Однією із головних частин є те, що запит надсилається до найближчого сервера від користувача. Для цього
був налаштований гео ДНС Gcore. Нижче наведена мапа, на якій показані зони дії кожного сервера.
<img src="https://i.ibb.co/TMxdhGK/image.png" alt="image" border="0">

На кожному сервері стоїть сервіс **Simple CDN server** який працює наступним чином:
- Користувач через головний сервер надсилає посилання для завантаження файлу найближчому файловому серверу
- Сервер завантажує та зберігає файл
- Сервер проводить реплікацію файла на інші сервери
- Файл стає доступним для завантаження на всих серверах

В результаті, завантажений файл збережений на всих серверах і швидкість його завантаження менше залежить від
розташування користувача завдяки багатьом серверам по світу.

## Про розробку
Подійно-орієнтована архітектура додатку спроектована із застосуванням принципу чистої архітектури,
де програма була поділена на шари, залежніть між якими була організована за допомогою Dependency Injection.

Розробка проводилась по принципу TDD, де перед розробкою функціоналу спочатку розробляються тести для нього,
в одночас формуються головні та додаткові, неочевидні вимоги.
Для швидкого та ефективного тестування були створені шари-імітації, що дозволило збільшити швидкість
під час модульного тестування.

Для автоматичних тестів та розгортання був застосований GitHub Actions. Для контейнеризації був застосований Docker.
