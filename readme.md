Задание 1.2

Краткая инструкция о реализации задания 1.2


Запускаем uvicorn

    uvicorn task1_2:app --reload

Отпраляем запрос на http://localhost:8000

    {
        "body": "https://hh.ru/vacancy/71240928?from=negotiations_item&hhtmFrom=negotiations_item"
    }

В ответе приходит сжатая ссылка
    
        http://localhost:8000/0

Отправляем заепрос на http://localhost:8000/0. Нас перенаправляет на нашу ссылку 


P.S код сопровожден коментариями


Задание 2.1

Необходимо: выбрать всех пользователей (user_id), которые впервые создали отчет в 2021-м году, и подсчитать сумму вознаграждений (reward) за 2022-й год в одном запросе

Тут непонятна формулировака. Если нам нужно получить все впервые созданные в 2021 году отчеты и просто рядом вывести сумму всех отчетов за 2022 то вот:

    SELECT *, (SELECT sum(reward) FROM reports2 WHERE EXTRACT(YEAR FROM created_at) = 2022) as sum
    FROM reports2 WHERE EXTRACT(YEAR FROM created_at) = 2021;

А если нам надо найти пользователей, которые выложили свой первый отчет в 2021 году и посчитать их суммы за 2022 то вот:


    WITH
    t1 as (SELECT * FROM reports WHERE EXTRACT(YEAR FROM created_at) = 2021),
    t2 as (SELECT * FROM reports WHERE EXTRACT(YEAR FROM created_at) < 2021),
    t3 as (SELECT t1.user_id FROM t1 LEFT JOIN t2 ON t1.user_id = t2.user_id WHERE t2.user_id is NULL GROUP BY t1.user_id)
    SELECT t3.user_id, sum(reward) FROM t3 JOIN reports on t3.user_id = reports.user_id WHERE EXTRACT(YEAR FROM created_at) = 2022 GROUP BY t3.user_id
    ;

Порядок выпонения:

1) Находим все записи которые были до 2021
2) Находим записи которые есть в 2021
3) Объединяем таблицы, оставляя только те записи которые появились в 2021
4) Объединяем таблицы, оставляя только те о которых есть упоменангие в 2021 году и считаем сумму


Задание 2.2

Необходимо: использовав агрегатные функции, выбрать все шк и цены (reports.barcode, reports.barcode) с одинаковыми названиями точек продаж (pos.title).

Здесь тоже непонятно. Если мы хотим получить  все шк и цены с одинаковыми названиями точек продаж, нам нужно вывести все шк и цен для одной точки? Так у этих шк и цен будет общая точка

    SELECT barcode FROM barcode WHERE pos_id = n

Где n это необходимая точка продаж

Если требуется вывести одинаковые данные не зная id точки, а только ее название, то вот

    SELECT barcode, price FROM reports JOIN pos p on reports.pos_id = p.id WHERE p.title = 'Name'

Где Name это название точки

Но возникает вопрос зачем нам тогда агрегатные функции? Может надо вывести общую сумму товаров для каждой точки?

    SELECT p.title, sum(price) FROM reports JOIN pos p on reports.pos_id = p.id GROUP BY p.title

P.S.S Спасибо за задние. Надеюсь на скорый ответ и разбор задачек.