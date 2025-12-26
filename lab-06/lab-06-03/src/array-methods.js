// src/array-methods.js

export const products = [
    { id: 1, name: 'iPhone', price: 999, category: 'electronics', inStock: true },
    { id: 2, name: 'MacBook', price: 1999, category: 'electronics', inStock: false },
    { id: 3, name: 'T-shirt', price: 29, category: 'clothing', inStock: true },
    { id: 4, name: 'Jeans', price: 79, category: 'clothing', inStock: true },
    { id: 5, name: 'Book', price: 15, category: 'education', inStock: false }
];

export const runArrayDemos = () => {
    console.log('\n--- Array Methods ---');

    // 1. Map: Получить имена
    const names = products.map(p => p.name);
    console.log('Names:', names);

    // 2. Filter: Только в наличии
    const available = products.filter(p => p.inStock);
    console.log('In Stock Count:', available.length);

    // 3. Reduce: Группировка по категориям
    const byCategory = products.reduce((acc, product) => {
        const cat = product.category;
        if (!acc[cat]) acc[cat] = [];
        acc[cat].push(product.name);
        return acc;
    }, {});
    console.log('Grouped by Category:', byCategory);
};
