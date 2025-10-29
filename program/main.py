import random
import matplotlib.pyplot as pltObj
import numpy as np
import pandas as pd
import sys
import os

from dotenv import load_dotenv

# обьект хранения данных
class Storage:
    numbersStorage = []  # массив данных
    pandasSeries = pd.Series()  # обьект Series из panda
    pandasDf = pd.DataFrame()  # обьект Dataframe из panda

    def __init__(self, needNumbersCount, minValue, maxValue):
        # генерация чисел
        for i in range(0, needNumbersCount):
            self.numbersStorage.append(
                random.randrange(
                    minValue,
                    maxValue
                )
            )

        # создание обьектов для работы
        self.pandasSeries = pd.Series(self.numbersStorage)
        self.pandasDf = pd.DataFrame({'Данные': self.pandasSeries})

    def findDuplicates(self, df):
        return len(df) - len(df.drop_duplicates())

    def getSeries(self):
        return self.pandasSeries

    def getDf(self):
        return self.pandasDf

    def getNumbers(self):
        return self.numbersStorage

    def findMinNumberFromStorage(self):
        return self.pandasSeries.min()

    def findMaxNumberFromStorage(self):
        return self.pandasSeries.max()

    def sumOfStorage(self):
        return self.pandasSeries.sum()

    def findNumbersStorageDuplicates(self, roundedToHundreds=False):
        if (roundedToHundreds):
            return self.findDuplicates(storage.pandasDf.round(decimals=-2))
        else:
            return self.findDuplicates(self.pandasDf)


# основная программа
if __name__ == '__main__':
    # направляем вывод консоли в файл
    sys.stdout = open('./output/output.txt', 'w+', encoding='UTF-16')

    # Подготавливаем приложение к работе
    NumbersGenerateCountCOUNT = 10000
    NumbersGenerateMinVal = -10000
    NumbersGenerateMaxVal = 10000

    # загружаем переменные окружения
    if not load_dotenv():
        print("Файл конфигурации .env не обнаружен")
        print("Для выполнения программы будут использованы дефолтные значения")
    else:
        # если существует файл конфигурации, то не будем использовать дефолтные значения
        NumbersGenerateCountCOUNT = int(os.environ.get('NUMBERS_GENERATE_COUNT'))
        NumbersGenerateMinVal = int(os.environ.get('NUMBERS_GENERATE_MIN_VAL'))
        NumbersGenerateMaxVal = int(os.environ.get('NUMBERS_GENERATE_MAX_VAL'))

    # если по каким то причинам минимальное значение больше максимального, то поменяем их местами
    if NumbersGenerateMinVal > NumbersGenerateMaxVal:
        NumbersGenerateMinVal, NumbersGenerateMaxVal = NumbersGenerateMaxVal, NumbersGenerateMinVal

    print(f'Колличество чисел для генерации: {NumbersGenerateCountCOUNT} в диапазоне от {NumbersGenerateMinVal} до {NumbersGenerateMaxVal}')


    # инициализация склада чисел и генерация 
    storage = Storage(NumbersGenerateCountCOUNT, NumbersGenerateMinVal, NumbersGenerateMaxVal)

    dataFrameTable = pd.DataFrame({'Данные': storage.getSeries()})
    dataFrameTable['Возрастание'] = storage.getSeries().sort_values().reset_index(drop=True)
    dataFrameTable['Убывание'] = storage.getSeries().sort_values(ascending=False).reset_index(drop=True)

    # выводим все необходимые по заданию значения в консоль
    print('Минимальное значение: %s' % (storage.findMinNumberFromStorage()))
    print('Колличество повторяемых более одного раза чисел: %s' % (storage.findNumbersStorageDuplicates()))
    print('Максимальное значение: %s' % (storage.findMaxNumberFromStorage()))
    print('Сумма чисел: %s' % (storage.sumOfStorage()))

    # Вывод DataFrame
    print(dataFrameTable)

    # рисуем графики и гистограммы:
    pltObj.figure(figsize=(20, 15), dpi=200)

    # линейный график сгенерированных чисел
    pltObj.subplot(2, 2, 1)
    pltObj.title('Линейный график')
    pltObj.plot(storage.getNumbers())
    pltObj.legend(["значение сгенерированных чисел"], fontsize="x-small")

    # линейные графики убывания и возрастания отосртированных чисел
    pltObj.subplot(2, 2, 2)
    pltObj.title('Убывание и возрастания')
    pltObj.plot(sorted(storage.getNumbers()), label='По возрастанию', marker='.')
    pltObj.plot(sorted(storage.getNumbers(), reverse=True), label='По убыванию', marker='.')
    pltObj.legend()

    # гисторграмма повторяющихся округленных до сотен чисел
    rounded_sorted_dict = storage.getDf().round(decimals=-2).groupby(
        storage.getDf().round(decimals=-2).columns.tolist(), as_index=False).size()

    x_indexes = np.arange(len(rounded_sorted_dict))
    pltObj.subplot(2, 1, 2)
    pltObj.title('Гистограмма округлённых до сотен значений')
    pltObj.xticks(x_indexes, rounded_sorted_dict["Данные"])
    pltObj.xticks(rotation=90, fontsize=5)
    pltObj.bar(x_indexes, list(rounded_sorted_dict["size"]))
    pltObj.legend(["кол-во совпадений"], fontsize="x-small")

    # сохраняем результат
    pltObj.savefig('./output/output.png')
