// src/async-fp.js

// Симуляция API
const fakeApi = (id) => new Promise(resolve => {
    setTimeout(() => resolve({ id, data: `User ${id}` }), 500);
});

export const runAsyncDemos = async () => {
    console.log('\n--- Async FP ---');

    const ids = [1, 2, 3];

    // Параллельная загрузка функционально
    console.log('Loading users...');
    const promises = ids.map(id => fakeApi(id));
    const users = await Promise.all(promises);

    console.log('Users loaded:', users.map(u => u.data));
};
