module Types where

-- Перечисление
data Day = Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday
    deriving (Show, Eq)

isWeekend :: Day -> Bool
isWeekend Saturday = True
isWeekend Sunday = True
isWeekend _ = False

-- Продуктовый тип
data Point = Point Double Double
    deriving (Show)

distance :: Point -> Point -> Double
distance (Point x1 y1) (Point x2 y2) = sqrt ((x2 - x1)^2 + (y2 - y1)^2)

-- Рекурсивный тип данных (список)
data List a = Empty | Cons a (List a)
    deriving (Show)

-- Функция для преобразования нашего списка в стандартный
toStandardList :: List a -> [a]
toStandardList Empty = []
toStandardList (Cons x xs) = x : toStandardList xs
