library(R6)

Microwave <- R6Class(
  "Microwave",
  
  private = list(
    power = 0,        # Мощность в Вт
    door_open = FALSE # Состояние дверцы: FALSE = закрыта
  ),
  
  public = list(
    # Конструктор
    initialize = function(power = 800, door_open = FALSE) {
      private$power <- power
      private$door_open <- door_open
    },
    
    # Метод открытия двери
    open_door = function() {
      private$door_open <- TRUE
      cat("Дверца открыта.\n")
    },
    
    # Метод закрытия двери
    close_door = function() {
      private$door_open <- FALSE
      cat("Дверца закрыта.\n")
    },
    
    # Метод приготовления пищи
    # Аргумент required_energy - условные единицы энергии для готовки
    cook = function(required_energy = 1000) {
      if (private$door_open) {
        cat("Ошибка: Нельзя включить микроволновку с открытой дверцей!\n")
      } else {
        cat(sprintf("Начинаю готовку (Мощность: %d Вт)...\n", private$power))
        
        # Время зависит от мощности: чем больше мощность, тем меньше время
        # time = энергия / мощность
        cook_time <- required_energy / private$power
        
        # Sys.sleep принимает секунды
        Sys.sleep(cook_time) 
        
        cat("Пища готова!\n")
      }
    }
  )
)

# --- Демонстрация работы ---

cat("\n--- Тест Микроволновки 1 (По умолчанию) ---\n")
oven_default <- Microwave$new() # По умолчанию 800 Вт
oven_default$cook(1600) # Должно занять 2 секунды

cat("\n--- Тест Микроволновки 2 (Мощная) ---\n")
oven_powerful <- Microwave$new(power = 1600, door_open = TRUE) # 1600 Вт, открыта
oven_powerful$cook(1600) # Ошибка - дверь открыта
oven_powerful$close_door()
oven_powerful$cook(1600) # Должно занять 1 секунду (быстрее)