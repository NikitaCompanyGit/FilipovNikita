# 1. Создаем дженерик функцию
get_area <- function(x, ...) {
  UseMethod("get_area")
}

# 2. Метод по умолчанию (если класс не определен или не поддерживается)
get_area.default <- function(x, ...) {
  message("Невозможно обработать данные: неизвестный класс фигуры")
}

# 3. Класс "rectangle" (прямоугольник). Вектор: c(ширина, высота)
get_area.rectangle <- function(x, ...) {
  if(length(x) < 2) stop("Для прямоугольника нужны ширина и высота")
  return(x[1] * x[2])
}

# 4. Класс "circle" (круг). Вектор: c(радиус)
get_area.circle <- function(x, ...) {
  return(pi * x[1]^2)
}

# --- Демонстрация работы ---

# Создаем векторы и присваиваем им классы
rect_params <- c(10, 5)
class(rect_params) <- "rectangle"

circle_params <- c(5)
class(circle_params) <- "circle"

unknown_params <- c(1, 2, 3)

# Вызов методов
print(paste("Площадь прямоугольника:", get_area(rect_params)))
print(paste("Площадь круга:", get_area(circle_params)))
get_area(unknown_params) # Выведет сообщение об ошибке