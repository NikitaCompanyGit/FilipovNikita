PiggyBank <- R6Class(
  "PiggyBank",
  
  private = list(
    balance = 0,    # Текущая сумма
    is_broken = FALSE # Цела ли копилка
  ),
  
  public = list(
    initialize = function(initial_amount = 0) {
      private$balance <- initial_amount
    },
    
    # Добавить монеты
    add_money = function(amount) {
      if (private$is_broken) {
        cat("Копилка разбита. Нельзя положить деньги.\n")
      } else {
        if (amount > 0) {
          private$balance <- private$balance + amount
          cat(sprintf("Добавлено %s монет. *Звяк*\n", amount))
        } else {
          cat("Сумма должна быть положительной.\n")
        }
      }
    },
    
    # Потрясти копилку (узнать, есть ли деньги, не разбивая)
    shake = function() {
      if (private$is_broken) {
        cat("Осколки гремят...\n")
      } else if (private$balance > 0) {
        cat("Внутри что-то звенит!\n")
      } else {
        cat("Тишина... Копилка пуста.\n")
      }
    },
    
    # Разбить копилку и забрать деньги
    break_bank = function() {
      if (private$is_broken) {
        cat("Она уже разбита.\n")
        return(0)
      } else {
        amount <- private$balance
        private$balance <- 0
        private$is_broken <- TRUE
        cat(sprintf("БАМ! Копилка разбита. Вы достали %s монет.\n", amount))
        return(amount)
      }
    }
  )
)

# --- Демонстрация работы ---
cat("\n--- Тест Копилки ---\n")
my_bank <- PiggyBank$new()
my_bank$shake()          # Пусто
my_bank$add_money(50)    # Кладем 50
my_bank$add_money(100)   # Кладем 100
my_bank$shake()          # Звенит
cash <- my_bank$break_bank() # Разбиваем, получаем 150
my_bank$add_money(10)    # Нельзя, разбита