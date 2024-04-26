import numpy as np

# Создаем генератор случайных чисел
rng = np.random.default_rng()

# Генерируем 1000 чисел из нормального распределения с loc=0 и scale=1
numbers = rng.normal(loc=0, scale=1, size=1000)

# Выбираем 5 случайных индексов
indices = rng.choice(np.arange(1000), size=995, replace=False)

# Устанавливаем значения по выбранным индексам равными 0
numbers[indices] = 0

# Проверяем, что только 5 из 1000 значений равны 0
print(np.sum(numbers == 0)) # Должно быть равно 5
print(numbers)