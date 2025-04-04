import pygame  # Импортируем библиотеку pygame для работы с графикой и событиями
import sys  # Импортируем sys для выхода из игры
import random  # Импортируем random для генерации случайных координат яблока

pygame.init()  # Инициализируем pygame

# Устанавливаем ширину и высоту экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
# Размер одного блока (ячейки), в котором будет двигаться змея
BLOCK_DIM = 40
# Создаем шрифт для отображения текста (размер зависит от BLOCK_DIM)
FONT = pygame.font.Font(None, BLOCK_DIM * 2)

# Создаем игровое окно
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Устанавливаем заголовок окна
pygame.display.set_caption("Snake Game")
# Создаем объект Clock для управления частотой кадров
clock = pygame.time.Clock()

# Класс змеи
class Snake:
    def __init__(self):  # Конструктор класса
        self.reset()  # Вызываем метод reset для инициализации змеи

    def reset(self):  # Метод сброса змеи (при старте игры или смерти)
        self.x, self.y = BLOCK_DIM, BLOCK_DIM  # Начальные координаты головы змеи
        self.x_direction = 1  # Начальное движение вправо (по X)
        self.y_direction = 0  # Начальное движение без изменения по Y
        # Создаем голову змеи (прямоугольник)
        self.head = pygame.Rect(self.x, self.y, BLOCK_DIM, BLOCK_DIM)
        # Создаем тело змеи, состоящее из одного блока позади головы
        self.body = [pygame.Rect(self.x - BLOCK_DIM, self.y, BLOCK_DIM, BLOCK_DIM)]
        self.dead = False  # Флаг состояния змеи (жива/мертва)

    def update(self):  # Метод обновления позиции змеи
        # Проверяем, не вышла ли змея за границы экрана
        if not (0 <= self.head.x < SCREEN_WIDTH and 0 <= self.head.y < SCREEN_HEIGHT):
            self.reset()  # Если вышла, сбрасываем игру

        # Проверяем, не столкнулась ли голова змеи с её телом
        for segment in self.body:
            if self.head.x == segment.x and self.head.y == segment.y:
                self.reset()  # Если столкнулась, сбрасываем игру

        # Добавляем копию головы в конец тела перед движением
        self.body.append(self.head.copy())
        # Двигаем голову змеи в соответствии с направлением
        self.head.x += self.x_direction * BLOCK_DIM
        self.head.y += self.y_direction * BLOCK_DIM
        # Удаляем последний элемент тела (так змея остается той же длины)
        self.body.pop(0)

# Класс яблока
class Apple:
    def __init__(self):  # Конструктор класса
        self.spawn()  # Создаем новое яблоко в случайной позиции

    def spawn(self):  # Метод генерации нового яблока
        # Выбираем случайные координаты внутри игрового поля, кратные BLOCK_DIM
        self.x = random.randint(0, (SCREEN_WIDTH // BLOCK_DIM) - 1) * BLOCK_DIM
        self.y = random.randint(0, (SCREEN_HEIGHT // BLOCK_DIM) - 1) * BLOCK_DIM
        # Создаем объект-прямоугольник для яблока
        self.rect = pygame.Rect(self.x, self.y, BLOCK_DIM, BLOCK_DIM)

    def draw(self):  # Метод отрисовки яблока
        pygame.draw.rect(screen, "red", self.rect)  # Рисуем красный квадрат

# Функция для отрисовки сетки на игровом поле
def draw_grid():
    for x in range(0, SCREEN_WIDTH, BLOCK_DIM):  # Проходим по горизонтали
        for y in range(0, SCREEN_HEIGHT, BLOCK_DIM):  # Проходим по вертикали
            rect = pygame.Rect(x, y, BLOCK_DIM, BLOCK_DIM)  # Создаем ячейку
            pygame.draw.rect(screen, "#444444", rect, 1)  # Рисуем рамку серого цвета

# Создаем экземпляры объектов змеи и яблока
snake = Snake()
apple = Apple()
speed = 5  # Начальная скорость игры

# Основной игровой цикл
while True:
    for event in pygame.event.get():  # Обрабатываем события pygame
        if event.type == pygame.QUIT:  # Проверяем, не нажата ли кнопка выхода
            pygame.quit()  # Закрываем pygame
            sys.exit()  # Выходим из программы

        if event.type == pygame.KEYDOWN:  # Проверяем, была ли нажата клавиша
            if event.key == pygame.K_DOWN and snake.y_direction == 0:
                # Если нажата стрелка вниз и змея не движется вверх, меняем направление
                snake.y_direction = 1
                snake.x_direction = 0
            elif event.key == pygame.K_UP and snake.y_direction == 0:
                # Если нажата стрелка вверх и змея не движется вниз, меняем направление
                snake.y_direction = -1
                snake.x_direction = 0
            elif event.key == pygame.K_RIGHT and snake.x_direction == 0:
                # Если нажата стрелка вправо и змея не движется влево, меняем направление
                snake.y_direction = 0
                snake.x_direction = 1
            elif event.key == pygame.K_LEFT and snake.x_direction == 0:
                # Если нажата стрелка влево и змея не движется вправо, меняем направление
                snake.y_direction = 0
                snake.x_direction = -1

    snake.update()  # Обновляем положение змеи

    screen.fill('black')  # Очищаем экран, заполняя его черным цветом
    draw_grid()  # Рисуем сетку
    apple.draw()  # Отображаем яблоко

    # Отображаем тело змеи
    for segment in snake.body:
        pygame.draw.rect(screen, "green", segment)  # Рисуем зеленые сегменты тела

    pygame.draw.rect(screen, "blue", snake.head)  # Рисуем голову змеи светло-зеленым

    # Создаем текст с очками и уровнем
    score_text = FONT.render(f"Score: {len(snake.body)}", True, "white")
    level_text = FONT.render(f"Level: {1 + len(snake.body) // 4}", True, "white")
    # Отображаем текст на экране
    screen.blit(score_text, (20, 20))
    screen.blit(level_text, (20, 80))

    # Проверяем, съела ли змея яблоко
    if snake.head.colliderect(apple.rect):
        # Если съела, увеличиваем тело змеи
        snake.body.append(snake.body[-1].copy())
        apple.spawn()  # Генерируем новое яблоко

    pygame.display.update()  # Обновляем экран
    clock.tick(speed + len(snake.body) // 4)  # Устанавливаем скорость игры
