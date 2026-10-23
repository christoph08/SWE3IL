#from testing_course.exploration.calculator import Calculator
from testing_course.exploration.person_repository import InMemoryPersonRepository

# calc = Calculator()
# calc.add("1", 2)
# calc.add(1)
# total: str = calc.multiply(1, 3)

repo = InMemoryPersonRepository()
print(repo.read_person_by_id(0).name)