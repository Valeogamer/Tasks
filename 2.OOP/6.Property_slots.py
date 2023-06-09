# Используем сет/гет а также проперти ТОЛЬКО при наличии логики в получении или установке атрибутов
#
# Возможность установки/получения атрибутов с логикой
# Запретить менять атрибут или добавлять новые атрибуты
# __dict__ - это атрибут объектов в питоне, который хранит состояние
# setattr__ - вызывается при попытке установить атрибут, то есть теперь при любой установке
# c помощью @property мы можем задавать некоторый getter и setter для некоторого атрибута
# для gettera даем имя @property, для setter имя нашего атрибута(функции)
# теперь как нам запретить создавать новые поля в логике @property
# __slots__ - создан для уменьшения памяти, занимаемой объектами,
# так как он заменяет словарь, на tuple, а как мы знаем еще, что tuple не изменяемый
# что работает как запрет добавления новых атрибутов, со словарем тоже можно, но нужжно писать условия
# также кортеж содержит итак кол - во атрибутов которые допустимы

from pympler import asizeof


class Cat:
    FIELDS = ('_name', '_age')  # допустимые поля
    __slots__ = ('_name', '_age')  # допустимые поля,

    # у класса есть зарезервированные поля и другие атрибуты добавить ему теперь нельзя

    def __init__(self, name, age):
        self.name = name  # функция сеттера должна совпдать с именем атрибута
        self.age = age

    def __repr__(self):
        return f'Cat name: {self.name}, age: {self.age}'

    # def __setattr__(self, key, value):
    #     # Теперь замена атрибута происзодит только по нашим правилам
    #     # Ни через init, ни через прямой вызов не сможем поменять атрибут без нашей логики
    #     # Запрещаем менять атрибут без наших правил
    #     if key not in self.FIELDS:
    #         # а теперь хотим еще запретить создавать новые атрибуты
    #         # проверка со string
    #         raise AttributeError(f"Допустимые поля: {self.FIELDS}")
    #     if key == 'name' and not value:
    #         raise AttributeError("Name cant be empty!")
    #     if key == 'age' and (value < 1 or value > 15):
    #         raise AttributeError("Age should be in 1 - 15!")
    #     self.__dict__[key] = value

    # теперь тоже самое что и сеттер попробуем сделать через проперти
    @property  # простой геттер, то что возвращает некоторое значение
    def name(self):
        return self._name

    @name.setter  # пишем имя того атрибута который мы будем сетить
    def name(self, value):
        # Теперь правила присвоения будут здесь
        if not value:
            raise AttributeError("Name cant be empty!")
        self._name = value

    @property
    def age(self):
        return self._age

    # Если есть геттер но нет сеттера, то установить атрибут невозможно
    # но сейчас у нас нет логики и проверки для наших атрибутов и вполне спокойно можем любое имя и возраст задать
    @age.setter
    def age(self, value):
        if value < 1 or value > 15:
            raise AttributeError("Age should be in 1 - 15!")
        self._age = value


class Empty:
    pass


if __name__ == '__main__':
    empty = Empty()
    empty.abra = 'cabra'
    print(empty.__dict__)
    tom = Cat("Tom", 11)
    # tom.age = 14  # теперь при таком изменении будет проверка через set, а не то через проверка через инит
    # проводилась всего лишь 1 раз
    # tom.name2 = "Cat" # пример для проверки допустимых полей
    print(tom)
    # string = "text"
    # string.x = 100  # Error запрет на создание новых атрибутов у класса string
    # Error AtribuError object has no atribute 'x'
    print(tom)
    print("Объект Том Занимает байт:", asizeof.asizeof(tom))  # сколько памяти занимает наш объект с двумя полями
    # если добавим еще один аргумент то перешагнем уже за 500 байт, и для борьбы с этим был придуман slots
    # после применения slots занимаемы размер в 3 раза уменьшился, а из за того что мы теперь работаем с кортежом,
    # а не со словарем
    print('stop')  # точка остановы
