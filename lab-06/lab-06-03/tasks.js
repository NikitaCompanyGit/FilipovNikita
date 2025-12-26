// tasks.js

// === Задание 1: Анализ пользователей ===
export const processUsers = (users) => {
    if (!users || users.length === 0) return null;

    const totalAge = users.reduce((acc, u) => acc + u.age, 0);

    // Группировка по городам
    const byCity = users.reduce((acc, u) => {
        acc[u.city] = (acc[u.city] || 0) + 1;
        return acc;
    }, {});

    // Email активных пользователей
    const activeEmails = users
        .filter(u => u.active)
        .map(u => u.email);

    return {
        averageAge: totalAge / users.length,
        usersPerCity: byCity,
        activeEmails: activeEmails
    };
};

// === Задание 2: Custom Hook (Симуляция логики) ===
// В реальном React мы бы импортировали useState
export const useFormLogic = (initialValues) => {
    // Эмуляция стейта для Node.js теста
    let values = { ...initialValues };

    const handleChange = (field, value) => {
        values = { ...values, [field]: value };
        return values; // Возвращаем новое состояние
    };

    const handleSubmit = (callback) => {
        if (values.email && values.password) {
            callback(values);
        } else {
            console.log('Validation failed');
        }
    };

    return { handleChange, handleSubmit };
};

// === Задание 3: Debounce ===
export const debounce = (func, delay) => {
    let timeoutId;
    return (...args) => {
        // Очищаем предыдущий таймер
        if (timeoutId) clearTimeout(timeoutId);

        // Ставим новый
        timeoutId = setTimeout(() => {
            func.apply(null, args);
        }, delay);
    };
};
