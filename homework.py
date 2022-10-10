from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> None:
        """Метод отвечает за вывод сообщения. """
        MSG_1 = (f'Тип тренировки: {self.training_type};'
                 f' Длительность: {self.duration:.3f} ч.;'
                 f' Дистанция: {self.distance:.3f} км;'
                 f' Ср. скорость: {self.speed:.3f} км/ч;'
                 f' Потрачено ккал: {self.calories:.3f}.')
        return MSG_1


class Training():
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    H_IN_M = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        train_dist = self.action * self.LEN_STEP / self.M_IN_KM
        return train_dist

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        try:
            self.get_spent_calories(self)
        finally:
            print(f'Метод get_spent_calories не переопределен'
                  f' в классе {self.__class__.__name__}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    COEF_CALORIES_1 = 18
    COEF_CALORIES_2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        run_spt_cal = ((self.COEF_CALORIES_1 * self.get_mean_speed()
                       - self.COEF_CALORIES_2) * self.weight / self.M_IN_KM
                       * self.duration * self.H_IN_M)
        return run_spt_cal


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WLK_COEF_CALORIES_1 = 0.035
    WLK_COEF_CALORIES_2 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        wlk_spt_cal = ((self.WLK_COEF_CALORIES_1 * self.weight
                       + (self.get_mean_speed() ** 2 // self.height)
                       * self.WLK_COEF_CALORIES_2 * self.weight)
                       * self.duration * self.H_IN_M)
        return wlk_spt_cal


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SWM_COEF_CALORIES_1 = 1.1
    SWM_COEF_CALORIES_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        swm_spt_cal = ((self.get_mean_speed() + self.SWM_COEF_CALORIES_1)
                       * self.SWM_COEF_CALORIES_2 * self.weight)
        return swm_spt_cal


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings = {'SWM': Swimming,
                 'RUN': Running,
                 'WLK': SportsWalking}
    if workout_type in trainings:
        result = trainings[workout_type](*data)
        return result
    else:
        return print('Данный вид тренировки не найден.')


def main(training: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info(training)
    msg = info.get_message()
    return print(msg)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
