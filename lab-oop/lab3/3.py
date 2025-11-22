
class MyName:
    """Опис класу / Документація
    """
    total_names = 0 #Class Variable

    def __init__(self, name=None) -> None:
        """Ініціалізація класу
        """
        self.name = name if name is not None else self.anonymous_user().name #Class attributes / Instance variables
        MyName.total_names += 1 #modify class variable
        self.my_id = self.total_names

    @property
    def whoami(self) -> str: 
        """Class property
        return: повертаємо імя 
        """
        return f"My name is {self.name}"
    
    @property
    def my_email(self) -> str:
        """Class property
        return: повертаємо емейл
        """
        return self.create_email()
    
    def create_email(self) -> str:
        """Instance method
        """
        return f"{self.name}@itcollege.lviv.ua"

    @classmethod
    def anonymous_user(cls):
        """Classs method
        """
        return cls("Anonymous")
    
    @staticmethod
    def say_hello(message="Hello to everyone!") -> str:
        """Static method
        """
        return f"You say: {message}"


print("Розпочинаємо створювати обєкти!")

names = ("Vadym", "Yana", None)
all_names = {name: MyName(name) for name in names}

for name, me in all_names.items():
    print(f"""{">*<"*20}
This is object: {me} 
This is object attribute: {me.name} / {me.my_id}
This is {type(MyName.whoami)}: {me.whoami} / {me.my_email}
This is {type(me.create_email)} call: {me.create_email()}
This is static {type(MyName.say_hello)} with defaults: {me.say_hello()} 
This is class variable {type(MyName.total_names)}: from class {MyName.total_names} / from object {me.total_names}
{"<*>"*20}""")

print(f"We are done. We create {me.total_names} names! ??? Why {MyName.total_names}?")


import os

class MyName:
    total_names = 0 

    def __init__(self, name=None) -> None:
        self.check_name(name) # Перевірка на валідацію перед створенням
        
        # Логіка з Anonymous
        if name is None:
            temp_user = self.anonymous_user()
            self.name = temp_user.name
        else:
            # Модифікуємо: завжди з великої літери
            self.name = name.capitalize()

        MyName.total_names += 1
        self.my_id = self.total_names

    @staticmethod
    def check_name(name):
        """Перевірка: ім'я може містити лише літери (якщо не None)"""
        if name is not None and not name.isalpha():
            raise ValueError(f"Помилка: Ім'я '{name}' може містити лише літери!")

    def count_letters(self) -> int:
        """Допишіть функцію: рахує кількість букв"""
        return len(self.name)

    # Змінюємо метод create_email (додаємо аргумент domain)
    def create_email(self, domain="itcollege.lviv.ua") -> str:
        return f"{self.name.lower()}@{domain}"

    @property
    def full_name(self) -> str:
        """Нова властивість: повертає розширений опис"""
        return f"User #{self.my_id}: {self.name} ({self.create_email()})"

    def save_to_file(self, filename="users.txt"):
        """Реалізуємо метод запису у файл"""
        with open(filename, "a", encoding="utf-8") as f:
            f.write(self.full_name + "\n")
        print(f"Дані користувача {self.name} збережено у {filename}")

    # --- Старі методи без змін ---
    @classmethod
    def anonymous_user(cls):
        return cls("Anonymous")
    
    @staticmethod
    def say_hello(message="Hello to everyone!") -> str:
        return f"You say: {message}"


# --- ПЕРЕВІРКА НОВОГО ФУНКЦІОНАЛУ ---

try:
    # 1. Створюємо список (додайте своє ім'я)
    names_list = ["Vadym", "Yana", None, "Ivan"] 
    
    print(f"{'='*10} Створення об'єктів {'='*10}")
    objects = [MyName(n) for n in names_list]

    for person in objects:
        # 2. Виводимо кількість букв
        print(f"Ім'я: {person.name}, Довжина: {person.count_letters()}")
        
        # 3. Виводимо full_name
        print(f"Full Info: {person.full_name}")
        
        # 4. Змінюємо email (модифікація після @)
        custom_email = person.create_email(domain="gmail.com")
        print(f"Custom Email: {custom_email}")

        # 5. Зберігаємо у файл
        person.save_to_file()
        print("-" * 20)

    # 6. Тест валідації (має викликати помилку)
    print("\nТестуємо помилку:")
    bad_user = MyName("Uesrrrr") 

except ValueError as e:
    print(f"ЗЛОВИЛИ ПОМИЛКУ: {e}")

print(f"\nЗагальна кількість створених об'єктів (лічильник класу): {MyName.total_names}")