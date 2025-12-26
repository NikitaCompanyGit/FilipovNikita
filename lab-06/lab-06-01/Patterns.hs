module Patterns where

-- Pattern matching для кортежей
addVectors :: (Double, Double) -> (Double, Double) -> (Double, Double)
addVectors (x1, y1) (x2, y2) = (x1 + x2, y1 + y2)

-- Работа с троичными кортежами
first :: (a, b, c) -> a
first (x, _, _) = x

second :: (a, b, c) -> b
second (_, y, _) = y

third :: (a, b, c) -> c
third (_, _, z) = z

-- Pattern matching в case выражениях
describeList :: [a] -> String
describeList xs = case xs of
    [] -> "Empty list"
    [x] -> "Singleton list"
    _ -> "Long list"
