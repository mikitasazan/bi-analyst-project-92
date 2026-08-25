import csv
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

REPO = os.path.dirname(os.path.abspath(__file__))

def read_csv(name):
    with open(f"{REPO}/{name}") as f:
        return list(csv.DictReader(f))

plt.rcParams.update({
    "font.size": 12,
    "figure.figsize": (11.69, 8.27),  # A4 landscape
})

DOW_ORDER = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DOW_RU = {"monday": "Пн", "tuesday": "Вт", "wednesday": "Ср", "thursday": "Чт",
          "friday": "Пт", "saturday": "Сб", "sunday": "Вс"}

pages = []

def title_page():
    fig, ax = plt.subplots()
    ax.axis("off")
    ax.text(0.5, 0.62, "Продажи", ha="center", va="center", fontsize=44, weight="bold")
    ax.text(0.5, 0.50, "Анализ данных торговой площадки", ha="center", va="center", fontsize=20)
    ax.text(0.5, 0.35, "SQL-анализ • сегментация покупателей • эффективность продавцов",
            ha="center", va="center", fontsize=13, color="gray")
    ax.text(0.5, 0.06, "Учебный проект Хекслета — github.com/mikitasazan/bi-analyst-project-92",
            ha="center", va="center", fontsize=10, color="gray")
    pages.append(fig)

def bar_page(title, labels, values, xlabel, ylabel, note, color="#4C72B0", horizontal=False):
    fig, ax = plt.subplots()
    if horizontal:
        ax.barh(labels, values, color=color)
        ax.invert_yaxis()
        ax.set_xlabel(ylabel)
    else:
        ax.bar(labels, values, color=color)
        ax.set_ylabel(ylabel)
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    ax.set_title(title, fontsize=18, weight="bold", pad=15)
    fig.text(0.5, 0.02, note, ha="center", fontsize=11, color="#333333", wrap=True)
    fig.tight_layout(rect=[0, 0.08, 1, 1])
    pages.append(fig)

# 1. Title
title_page()

# 2. Top-10 popular products (by quantity)
rows = read_csv("top_10_popular_products.csv")
labels = [r["ProductID"] for r in rows]
values = [int(r["TotalQuantity"]) for r in rows]
bar_page("Топ-10 товаров по количеству продаж", labels, values,
          "ProductID", "Продано штук",
          "Вывод: лидер по объёму — товар 463, с заметным отрывом от товара 399.")

# 3. Top-10 profitable products
rows = read_csv("top_10_profitable_products.csv")
labels = [r["ProductID"] for r in rows]
values = [int(r["Amount"]) for r in rows]
bar_page("Топ-10 товаров по выручке", labels, values,
          "ProductID", "Выручка",
          "Вывод: товар 276 приносит наибольшую выручку — почти вдвое больше товара 280.")

# 4. Top-10 sellers by income
rows = read_csv("top_10_total_income.csv")
labels = [r["seller"] for r in rows]
values = [int(r["income"]) for r in rows]
bar_page("Топ-10 продавцов по суммарной выручке", labels, values,
          "Продавец", "Выручка",
          "Вывод: Dirk Stringer лидирует по выручке при сопоставимом с конкурентами числе сделок.",
          color="#55A868", horizontal=True)

# 5. Lowest average income sellers
rows = read_csv("lowest_average_income.csv")
labels = [r["seller"] for r in rows]
values = [int(r["average_income"]) for r in rows]
bar_page("Продавцы со средней выручкой ниже общей средней", labels, values,
          "Продавец", "Средняя выручка за сделку",
          "Вывод: у этой группы продавцов средний чек заметно ниже общего — потенциал для обучения.",
          color="#C44E52", horizontal=True)

# 6. Income by day of week (aggregated across sellers)
rows = read_csv("day_of_the_week_income.csv")
totals = {d: 0 for d in DOW_ORDER}
for r in rows:
    totals[r["day_of_week"].strip()] += int(r["income"])
labels = [DOW_RU[d] for d in DOW_ORDER]
values = [totals[d] for d in DOW_ORDER]
bar_page("Суммарная выручка по дням недели", labels, values,
          "День недели", "Выручка",
          "Вывод: выручка распределена по будням достаточно равномерно, явного пика нет.",
          color="#8172B2")

# 7. Age groups
rows = read_csv("age_groups.csv")
order = ["16-25", "26-40", "40+"]
counts = {r["age_category"]: int(r["age_count"]) for r in rows}
labels = order
values = [counts[c] for c in order]
fig, ax = plt.subplots()
colors = ["#4C72B0", "#55A868", "#C44E52"]
ax.pie(values, labels=[f"{l}\n{v} чел." for l, v in zip(labels, values)],
       autopct="%1.0f%%", colors=colors, startangle=90)
ax.set_title("Возрастная структура покупателей", fontsize=18, weight="bold", pad=15)
fig.text(0.5, 0.03, "Вывод: основная аудитория площадки — покупатели старше 40 лет.",
          ha="center", fontsize=11, color="#333333")
pages.append(fig)

# 8. Customers & income by month
rows = read_csv("customers_by_month.csv")
months = [r["selling_month"] for r in rows]
customers = [int(r["total_customers"]) for r in rows]
income = [int(r["income"]) for r in rows]
fig, ax1 = plt.subplots()
ax1.bar(months, income, color="#4C72B0", alpha=0.7, label="Выручка")
ax1.set_ylabel("Выручка")
ax2 = ax1.twinx()
ax2.plot(months, customers, color="#C44E52", marker="o", linewidth=2, label="Покупатели")
ax2.set_ylabel("Уникальных покупателей")
ax1.set_title("Выручка и число покупателей по месяцам", fontsize=18, weight="bold", pad=15)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")
fig.text(0.5, 0.02, "Вывод: динамика покупателей и выручки согласована по месяцам наблюдения.",
          ha="center", fontsize=11, color="#333333")
fig.tight_layout(rect=[0, 0.06, 1, 1])
pages.append(fig)

# 9. Special offer first-purchase customers
rows = read_csv("special_offer.csv")
fig, ax = plt.subplots()
ax.axis("off")
ax.text(0.5, 0.85, "Первая покупка по акции", ha="center", fontsize=20, weight="bold")
ax.text(0.5, 0.72, f"{len(rows)} покупателей начали знакомство с площадкой с акционного товара",
        ha="center", fontsize=13)
table_rows = [[r["customer"], r["sale_date"], r["seller"]] for r in rows[:10]]
tbl = ax.table(cellText=table_rows, colLabels=["Покупатель", "Дата", "Продавец"],
               loc="center", cellLoc="center", bbox=[0.1, 0.05, 0.8, 0.6])
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
pages.append(fig)

# 10. Conclusion
fig, ax = plt.subplots()
ax.axis("off")
ax.text(0.5, 0.9, "Выводы", ha="center", fontsize=26, weight="bold")
bullets = [
    "Товар 463 — лидер и по количеству продаж, и близок к лидерству по выручке.",
    "Выручка компании сконцентрирована на топ-10 продавцах и топ-10 товарах.",
    "Есть группа продавцов со средним чеком ниже общего — точка роста для обучения.",
    "Основная аудитория площадки — покупатели старше 40 лет.",
    f"{len(read_csv('special_offer.csv'))} клиентов пришли через акции — акции работают как канал привлечения.",
    "Все запросы и код анализа — в queries.sql и *.csv в репозитории проекта.",
]
for i, b in enumerate(bullets):
    ax.text(0.07, 0.75 - i * 0.11, f"•  {b}", fontsize=13, va="top")
pages.append(fig)

with PdfPages(f"{REPO}/presentation.pdf") as pdf:
    for fig in pages:
        pdf.savefig(fig)
        plt.close(fig)

print("done, pages:", len(pages))
