import json
from datetime import datetime, timedelta

FILE_NAME = "events.json"


# Завантаження подій
def load_events():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return []


# Збереження подій
def save_events(events):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(events, file, indent=4, ensure_ascii=False)


# Вітання
def greeting():
    print("Вітаю! Я бот-організатор подій.")


# Допомога
def help_command():
    print("""
Доступні команди:

додати
показати
події_тиждень
події_сьогодні
події_завтра
найближча
фільтр_дата
фільтр_категорія
редагувати
видалити
допомога
вийти
""")


# Перевірка конфлікту
def check_conflict(events, new_date, new_time):
    for event in events:
        if event["date"] == new_date and event["time"] == new_time:
            return True
    return False


# Додати подію
def add_event(events):
    name = input("Назва події: ")
    date = input("Дата (YYYY-MM-DD): ")
    time = input("Час (HH:MM): ")
    category = input("Категорія: ")

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Неправильний формат дати! Використовуйте YYYY-MM-DD")
        return

    if check_conflict(events, date, time):
        print("Увага! Конфлікт у розкладі.")

    event = {
        "name": name,
        "date": date,
        "time": time,
        "category": category
    }

    events.append(event)
    save_events(events)
    print("Подію додано.")


# Показати всі події
def show_events(events):
    if not events:
        print("Подій немає.")
        return

    for i, event in enumerate(events):
        print(f"{i}. {event['name']} | {event['date']} {event['time']} | {event['category']}")


# Події на тиждень
def events_week(events):

    today = datetime.today().date()
    week = today + timedelta(days=7)

    for event in events:
        try:
            event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
        except ValueError:
            continue

        if today <= event_date <= week:
            print(event)


# Події сьогодні
def today_events(events):
    today = datetime.today().strftime("%Y-%m-%d")

    for event in events:
        if event["date"] == today:
            print(event)


# Події завтра
def tomorrow_events(events):
    tomorrow = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")

    for event in events:
        if event["date"] == tomorrow:
            print(event)


# Найближча подія
def nearest_event(events):

    if not events:
        print("Подій немає")
        return

    now = datetime.now()
    nearest = None

    for event in events:
        try:
         event_time = datetime.strptime(
            event["date"] + " " + event["time"],
            "%Y-%m-%d %H:%M"
        )
        except ValueError:
            continue

        if event_time > now:
            if nearest is None or event_time < nearest:
                nearest = event_time
                nearest_event_data = event

    if nearest:
        print("Найближча подія:", nearest_event_data)
    else:
        print("Немає майбутніх подій.")


# Фільтр по даті
def filter_date(events):
    date = input("Введіть дату: ")

    for event in events:
        if event["date"] == date:
            print(event)


# Фільтр по категорії
def filter_category(events):
    category = input("Категорія: ")

    for event in events:
        if event["category"] == category:
            print(event)


# Редагувати
def edit_event(events):
    show_events(events)

    index = int(input("Номер події: "))

    events[index]["name"] = input("Нова назва: ")
    events[index]["date"] = input("Нова дата: ")
    events[index]["time"] = input("Новий час: ")
    events[index]["category"] = input("Нова категорія: ")

    save_events(events)
    print("Подію змінено.")


# Видалити
def delete_event(events):
    show_events(events)

    index = int(input("Номер події для видалення: "))

    events.pop(index)

    save_events(events)
    print("Подію видалено.")


# Головна функція
def main():

    events = load_events()

    greeting()

    while True:

        command = input("\nВведіть команду: ").lower()

        if command == "додати":
            add_event(events)

        elif command == "показати":
            show_events(events)

        elif command == "події_тиждень":
            events_week(events)

        elif command == "події_сьогодні":
            today_events(events)

        elif command == "події_завтра":
            tomorrow_events(events)

        elif command == "найближча":
            nearest_event(events)

        elif command == "фільтр_дата":
            filter_date(events)

        elif command == "фільтр_категорія":
            filter_category(events)

        elif command == "редагувати":
            edit_event(events)

        elif command == "видалити":
            delete_event(events)

        elif command == "допомога":
            help_command()

        elif command == "вийти":
            print("До побачення!")
            break

        else:
            print("Невідома команда.")


main()