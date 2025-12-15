# Функция для расчета расходов (процедурный подход)
calculate_expenses <- function() {
  # 1. Запрос данных у пользователя (минимум 3 статьи)
  # В R interactive() проверяет, запущен ли код в интерактивной среде
  if (interactive()) {
    cat("Введите расходы на Продукты: ")
    cost1 <- as.numeric(readline())
    
    cat("Введите расходы на Коммунальные услуги: ")
    cost2 <- as.numeric(readline())
    
    cat("Введите расходы на Транспорт: ")
    cost3 <- as.numeric(readline())
  } else {
    # Значения по умолчанию для демонстрации (если запуск не интерактивный)
    cost1 <- 15000
    cost2 <- 5000
    cost3 <- 3000
    cat("Запуск в неинтерактивном режиме. Используются тестовые данные.\n")
  }
  
  # Проверка на корректность ввода (необязательно, но полезно)
  if (is.na(cost1) || is.na(cost2) || is.na(cost3)) {
    cat("Ошибка: Введены некорректные данные.\n")
    return(NULL)
  }
  
  # 2. Вычисления
  total_sum <- cost1 + cost2 + cost3
  max_expense <- max(cost1, cost2, cost3)
  
  # Определение названия максимальной статьи (дополнительная логика для удобства)
  expense_names <- c("Продукты", "Коммунальные услуги", "Транспорт")
  expense_values <- c(cost1, cost2, cost3)
  max_category <- expense_names[which.max(expense_values)]
  
  # 3. Вывод результатов
  cat("\n--- Отчет о расходах ---\n")
  cat(sprintf("Суммарные расходы за месяц: %.2f\n", total_sum))
  cat(sprintf("Максимальная статья расходов: %.2f (%s)\n", max_expense, max_category))
}

# Вызов процедуры
calculate_expenses()
