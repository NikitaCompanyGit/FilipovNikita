get_negative_values <- function(df) {
  # Список для хранения результатов по каждому столбцу
  results_list <- list()
  
  # Проходим по всем столбцам датафрейма
  for (col_name in names(df)) {
    column_data <- df[[col_name]]
    
    # Отбираем отрицательные значения, исключая NA
    neg_values <- column_data[!is.na(column_data) & column_data < 0]
    
    # Если есть отрицательные значения, сохраняем их
    if (length(neg_values) > 0) {
      results_list[[col_name]] <- neg_values
    }
  }
  
  # Если отрицательных значений нет вообще, возвращаем NULL
  if (length(results_list) == 0) {
    return(NULL)
  }
  
  # Проверяем, одинаковое ли количество элементов во всех найденных векторах
  # Получаем длины всех векторов в списке
  lengths <- sapply(results_list, length)
  
  # Если все длины равны длине первого элемента (и элементов > 0)
  if (all(lengths == lengths[1])) {
    # Возвращаем как датафрейм (матрицу)
    return(as.data.frame(results_list))
  } else {
    # Иначе возвращаем как список
    return(results_list)
  }
}

# --- Примеры использования (как на скриншоте) ---

# Пример 1: Разное количество отрицательных значений (должен быть список)
test_data1 <- as.data.frame(list(
  V1 = c(-9.7, -10, -10.5, -7.8, -8.9), 
  V2 = c(NA, -10.2, -10.1, -9.3, -12.2), 
  V3 = c(NA, NA, -9.3, -10.9, -9.8)
))
print("Результат 1 (Список):")
print(get_negative_values(test_data1))

# Пример 2: Отрицательные значения не во всех столбцах
test_data2 <- as.data.frame(list(
  V1 = c(NA, 0.5, 0.7, 8), 
  V2 = c(-0.3, NA, 2, 1.2), 
  V3 = c(2, -1, -5, -1.2)
))
print("Результат 2 (Список, без V1):")
print(get_negative_values(test_data2))

# Пример 3: Одинаковое количество отрицательных значений (должна быть матрица/df)
test_data3 <- as.data.frame(list(
  V1 = c(NA, -0.5, -0.7, -8), 
  V2 = c(-0.3, NA, -2, -1.2), 
  V3 = c(1, 2, 3, NA)
))
print("Результат 3 (Матрица/Dataframe):")
print(get_negative_values(test_data3))
