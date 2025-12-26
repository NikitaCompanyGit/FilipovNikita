module Main where

-- Импорт наших модулей (файлы должны лежать рядом)
import Basics
import Recursion
import Patterns
import HigherOrder
import Types

-- === Практические задания (Раздел 7) ===

-- Задание 1
countEven :: [Int] -> Int
countEven xs = length (filter even xs) -- Используем filter из стандартной библиотеки или filter' из HigherOrder

-- Задание 2
positiveSquares :: [Int] -> [Int]
positiveSquares xs = map (^2) (filter (>0) xs)

-- Задание 3 (Пузырьковая сортировка)
bubbleSort :: [Int] -> [Int]
bubbleSort [] = []
bubbleSort xs =
    let
        pass (x:y:rest)
            | x > y     = y : pass (x:rest)
            | otherwise = x : pass (y:rest)
        pass [x] = [x]
        pass [] = []

        passed = pass xs
        initialList = take (length xs - 1) passed
        lastElement = drop (length xs - 1) passed
    in
        if passed == xs
        then xs
        else bubbleSort initialList ++ lastElement


-- === Точка входа ===
main :: IO ()
main = do
    putStrLn "=== Lab 6 Execution ==="

    putStrLn "\n-- Basics --"
    print (square 5)

    putStrLn "\n-- Recursion --"
    print (factorial 5)

    putStrLn "\n-- Practical Tasks --"
    putStrLn "1. Count Even [1..10]:"
    print (countEven [1..10])

    putStrLn "2. Positive Squares [-2, -1, 0, 1, 2, 3]:"
    print (positiveSquares [-2, -1, 0, 1, 2, 3])

    putStrLn "3. Bubble Sort [4, 2, 5, 1, 3]:"
    print (bubbleSort [4, 2, 5, 1, 3])
