library(janeaustenr)
library(stringr)
library(dplyr)

# 1. Восстанавливаем функции из задания
extract_words <- function(book_name) {
  text <- subset(austen_books(), book == book_name)$text
  # Извлекаем слова, убираем списки и приводим к нижнему регистру
  str_extract_all(text, boundary("word")) %>% unlist %>% tolower
}

janeausten_words <- function() {
  books <- austen_books()$book %>% unique %>% as.character
  # Применяем extract_words ко всем книгам
  words <- sapply(books, extract_words) %>% unlist
  words
}

select_words <- function(letter, words, min_length = 1) {
  # Фильтр по длине
  min_length_words <- words[nchar(words) >= min_length]
  # Фильтр по первой букве (используем регулярное выражение: ^ - начало строки)
  grep(paste0("^", letter), min_length_words, value = TRUE)
}

max_frequency <- function(letter, words, min_length = 1) {
  w <- select_words(letter, words, min_length = min_length)
  # Если слов на эту букву нет, возвращаем 0
  if(length(w) == 0) return(structure(0, names="NA"))
  
  frequency <- table(w)
  # Возвращаем элемент с максимальной частотой (сохраняя имя слова)
  frequency[which.max(frequency)]
}

# 2. Выполнение основной логики задания
# Создаем вектор всех слов (это может занять несколько секунд)
all_words <- janeausten_words()

# Используем lapply, чтобы получить список результатов (сохраняя имена слов)
# letters - встроенная переменная R с буквами "a"..."z"
results_list <- lapply(letters, max_frequency, words = all_words, min_length = 5)

# Преобразуем список в вектор значений (частот)
counts <- unlist(results_list)

# Извлекаем имена (сами слова) из результатов для подписи осей
# Функция names() внутри sapply достанет слово (например, "could") из каждого элемента
word_labels <- sapply(results_list, names)

# 3. Визуализация
# las = 2 поворачивает подписи перпендикулярно оси для читаемости
barplot(counts, 
        names.arg = word_labels, 
        las = 2, 
        col = "grey",
        main = "Наиболее часто встречающиеся слова (>= 5 букв)",
        ylab = "Частота")