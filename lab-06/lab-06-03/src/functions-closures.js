// src/functions-closures.js

// Каррирование: функция возвращает функцию
export const multiply = a => b => a * b;

// Композиция функций (справа налево)
export const compose = (...fns) => x => fns.reduceRight((acc, fn) => fn(acc), x);

// Замыкание
export const createCounter = () => {
    let count = 0;
    return {
        inc: () => ++count,
        val: () => count
    };
};

export const runFunctionDemos = () => {
    console.log('\n--- Functions & Closures ---');

    const double = multiply(2);
    console.log('Currying (Double 5):', double(5));

    const add5 = x => x + 5;
    const square = x => x * x;

    // Сначала add5, потом square: (2 + 5)^2 = 49
    const addThenSquare = compose(square, add5);
    console.log('Composition (2+5)^2:', addThenSquare(2));
};
