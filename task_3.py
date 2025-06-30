"""3. Проанализировать и оптимизировать код ниже, перечислить внесенные изменения и обосновать их"""

"""Исходный код"""
def sum_numbers():
    file = open("numbers.txt", "r") # Используется open без with, файл останется открытым, если произойдёт исключение до file.close()
    data = file.readlines() # Чтение всего файла в память (readlines()), хотя можно итерироваться построчно для больших файлов
    sum = 0 # Переменная названа sum, что перекрывает встроенную функцию sum()
    for num in data:
        try:
            sum += int(num.strip())
        except: # except: без указания конкретного типа исключения, ловит все ошибки, даже неожиданные
            print("Ошибка при преобразовании числа:", num)
    print("Сумма чисел: " + str(sum)) # Конкатенация строк в print лучше заменяется f-строкой для читаемости
    file.close()

"""Оптимизированный код"""

def sum_numbers_optimize():
    total = 0
    try:
        with open("numbers.txt", "r") as file:
            for line in file:
                try:
                    total += int(line.strip())
                except ValueError:
                    print("Ошибка при преобразовании числа:", line.strip())
        print(f"Сумма чисел: {total}")
    except FileNotFoundError:
        print("Файл numbers.txt не найден.")


"""
Изменения

1.	Использован with open(...) as file	
2.	Переименована переменная sum в total	
3.	Использован цикл for line in file вместо readlines()	
4.	Добавлен except ValueError вместо общего except	
5.	Добавлен except FileNotFoundError если файла не существует	
6.	Использована f-строка в print	
"""

