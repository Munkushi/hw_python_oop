class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training():
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    M_IN_HOUR = 60
    coeff_cal1: float = 18
    coeff_cal2: float = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance_formula = self.action * self.LEN_STEP / self.M_IN_KM
        return distance_formula

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        average_speed_formula = self.get_distance() / self.duration
        return average_speed_formula

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
    pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        distance_formula = self.get_distance()
        average_speed_formula = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type,
                           self.duration,
                           distance_formula,
                           average_speed_formula,
                           calories)


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.coeff_cal1 * self.get_mean_speed() - self.coeff_cal2)
                * self.weight / self.M_IN_KM
                * self.duration * self.M_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    new_coeff_calorie_1: float = 0.035
    new_coeff_calorie_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return((self.new_coeff_calorie_1 * self.weight
               + (self.get_mean_speed()**2 // self.height)
               * self.new_coeff_calorie_2 * self.weight)
               * self.duration * Training.M_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.lenght_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + 1.1) * 2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_of_training = {
        'WLK': SportsWalking,
        'RUN': Running,
        'SWM': Swimming
    }
    if workout_type in type_of_training:
        return type_of_training.get(workout_type)(*data)
    else:
        return 'Вы где-то ошиблись :(.'


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
