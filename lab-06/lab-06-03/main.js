// main.js
import { runArrayDemos } from './src/array-methods.js';
import { runFunctionDemos } from './src/functions-closures.js';
import { runImmutabilityDemos } from './src/immutability.js';
import { runAsyncDemos } from './src/async-fp.js';

import { processUsers, debounce, useFormLogic } from './tasks.js';

const main = async () => {
    console.log('=== LAB 6: JS & FRONTEND ===');

    // 1. Запуск теории
    runArrayDemos();
    runFunctionDemos();
    runImmutabilityDemos();
    await runAsyncDemos(); // Ждем завершения асинхронной демки

    console.log('\n=== PRACTICAL TASKS ===');

    // Тест Задания 1
    console.log('\n--- Task 1: Users ---');
    const users = [
        { name: 'John', age: 25, city: 'NY', active: true, email: 'j@test.com' },
        { name: 'Jane', age: 30, city: 'NY', active: false, email: 'jane@test.com' },
        { name: 'Bob', age: 20, city: 'LA', active: true, email: 'bob@test.com' }
    ];
    console.log(processUsers(users));

    // Тест Задания 2 (Логика хука)
    console.log('\n--- Task 2: useForm Logic ---');
    const form = useFormLogic({ email: '', password: '' });
    console.log('Typing email...');
    const newState = form.handleChange('email', 'admin@site.com');
    console.log('New State:', newState);

    // Тест Задания 3 (Debounce)
    console.log('\n--- Task 3: Debounce ---');
    console.log('Simulating rapid typing...');
    const logTyped = debounce((text) => console.log('API Request for:', text), 500);

    logTyped('H');
    logTyped('He');
    logTyped('Hel');
    logTyped('Hello');
    // Должен вывестись только последний "Hello" через 500мс
};

main();
