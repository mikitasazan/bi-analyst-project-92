# Продажи

[![hexlet-check](https://github.com/mikitasazan/bi-analyst-project-92/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/mikitasazan/bi-analyst-project-92/actions)

Учебный проект курса «Аналитик данных» (Хекслет): анализ базы данных условной
торговой площадки. Задача — SQL-запросами и работой с Google Sheets ответить
на вопросы о самых продаваемых товарах, эффективности продавцов и поведении
покупателей, оформить результаты в отчёты и презентацию.

Учебный проект Хекслета: https://ru.hexlet.io/programs/bi-analyst

## Что внутри

| Файл | Как получен |
|---|---|
| `queries.sql` | Все SQL-запросы к базе `salesdb`, с комментарием перед каждым |
| `customers_count.csv`, `top_10_total_income.csv`, `lowest_average_income.csv`, `day_of_the_week_income.csv`, `age_groups.csv`, `customers_by_month.csv`, `special_offer.csv` | Результаты соответствующих запросов из `queries.sql` (по порядку) |
| `top_10_popular_products.csv`, `top_10_profitable_products.csv` | Из двух Google-таблиц с продажами и ценами товаров (SQL до них не достаёт — данные не в базе) |
| `presentation.pdf` | Презентация с графиками по всем отчётам выше и выводами |
| `build_presentation.py`, `requirements.txt` | Скрипт и зависимость, которыми `presentation.pdf` собирается из CSV — см. «Проверка локально» |

## Стек

- PostgreSQL — джойны, оконные функции, агрегаты, CTE
- Google Sheets — часть исходных данных отдаётся не из базы, а из таблиц
- Python (matplotlib) — сборка `presentation.pdf` из данных отчётов

## Установка

```bash
git clone https://github.com/mikitasazan/bi-analyst-project-92.git
cd bi-analyst-project-92
```

Для проверки SQL-части нужен клиент `psql` (`brew install libpq`, либо любой
дистрибутив PostgreSQL).

## Проверка локально

База данных учебная, доступ уже открыт для всех, credentials из условия
проекта:

```bash
export PGPASSWORD=student
```

**1. Запросы к базе.** Прогнать весь `queries.sql` и свериться с CSV-файлами
в репозитории (порядок вывода совпадает с порядком файлов в таблице выше):

```bash
psql -h db.hexlet.app -p 5432 -U student -d salesdb -f queries.sql
```

Чтобы получить готовый CSV, а не текстовую таблицу, — так же, как были
получены файлы в репозитории:

```bash
psql -h db.hexlet.app -p 5432 -U student -d salesdb \
  -c "\copy (SELECT count(*) AS customers_count FROM customers) TO 'customers_count.csv' WITH CSV HEADER"
```

**2. Отчёты по товарам.** Эти два файла считаются не из базы, а из двух
Google-таблиц (продажи и цены товаров), которые Хекслет даёт по ссылке на
шагах 2 и 4 проекта — сама Google Sheets Query API не умеет джойнить две
разные таблицы, поэтому подсчёт top-10 по выручке идёт локально. Для
самой выгрузки топ-10 по количеству (не требует джойна) хватает одного
запроса к Google Visualization API:

```bash
curl -sL "https://docs.google.com/spreadsheets/d/1Y_gzrFfOAJfTZo2u-PfU4selSic11dqM50bS3RlLA8M/gviz/tq?tqx=out:csv&tq=select+D,+sum(E)+group+by+D+order+by+sum(E)+desc+limit+10"
```

Должно совпасть с `top_10_popular_products.csv`.

Для `top_10_profitable_products.csv` нужна вторая таблица — с ценами товаров
(шаг 4); её ссылка нигде в этом репозитории не сохранена, только в тексте
шага на Хекслете. Если этот шаг снова понадобится пройти с нуля, ссылку
придётся взять там заново — из самого репозитория `top_10_profitable_products.csv`
не переcобрать.

**3. Презентация.** `build_presentation.py` пересобирает `presentation.pdf`
из уже готовых CSV — графики по каждому отчёту плюс слайд с выводами:

```bash
pip install -r requirements.txt
python3 build_presentation.py
```

---

<details>
<summary>Автоматические тесты Хекслета</summary>

Тесты запускаются на каждый коммит. За запуск отвечает файл `.github/workflows/hexlet-check.yml` — не удаляйте и не переименовывайте ни его, ни репозиторий.

</details>

## О Хекслете

[Хекслет](https://ru.hexlet.io/) — школа программирования: авторские программы обучения с практикой, поддержкой наставников и реальными проектами, которые остаются в резюме. Этот репозиторий — один из таких проектов.
