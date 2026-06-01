import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv

from google.adk import Agent

load_dotenv()

# ==========================================
# 1. АБСТРАКЦІЯ
# ==========================================
class Person(ABC):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    @abstractmethod
    def get_role(self) -> str:
        pass

# ==========================================
# 2. НАСЛІДУВАННЯ
# ==========================================
class Student(Person):
    def __init__(self, name: str, age: int):
        super().__init__(name, age)
        # ==========================================
        # 3. ІНКАПСУЛЯЦІЯ (приватний атрибут __grades)
        # ==========================================
        self.__grades = [] 

    def add_grade(self, grade: float):
        if grade >= 0:
            self.__grades.append(grade)

    def average(self) -> float:
        return sum(self.__grades) / len(self.__grades) if self.__grades else 0.0

    def min_grade(self) -> float:
        return min(self.__grades) if self.__grades else 0.0

    def max_grade(self) -> float:
        return max(self.__grades) if self.__grades else 0.0

    # ==========================================
    # 4. ПОЛІМОРФІЗМ
    # ==========================================
    def get_role(self) -> str:
        return "Студент"

class Teacher(Person):
    def __init__(self, name: str, age: int, subject: str):
        super().__init__(name, age)
        self.subject = subject

    def get_role(self) -> str:
        return "Викладач"

    def evaluate(self, student: Student, grade: float):
        student.add_grade(grade)

# ==========================================
# ІНСТРУМЕНТ ДЛЯ АГЕНТА (Звичайна функція)
# ==========================================
def calculate_grade(name: str, scores: list) -> dict:
    """Обчислює середній бал, мін/макс оцінку та буквений рейтинг."""
    student = Student(name=name, age=18)
    
    for score in scores:
        student.add_grade(float(score))

    avg = student.average()
    
    if avg >= 90:
        letter_grade = "A"
    elif avg >= 75:
        letter_grade = "B"
    elif avg >= 60:
        letter_grade = "C"
    else:
        letter_grade = "F"

    return {
        "student": student.name,
        "average": round(avg, 2),
        "min": student.min_grade(),
        "max": student.max_grade(),
        "letter_grade": letter_grade
    }

# ==========================================
# НАЛАШТУВАННЯ АГЕНТА
# ==========================================
agent_prompt = """Ти — освітній асистент. 
1. Використовуй інструмент calculate_grade для розрахунку балів.
2. Повідомляй рейтинг, середній бал, найвищу та найнижчу оцінки.
3. Давай поради щодо покращення успішності. 
Відповідай українською мовою."""

root_agent = Agent(
    name="StudentPerformanceAgent",
    instruction=agent_prompt,  # <--- ВИПРАВЛЕНО: instruction замість instructions
    tools=[calculate_grade]
)