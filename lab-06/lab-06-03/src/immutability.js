// src/immutability.js

export const runImmutabilityDemos = () => {
    console.log('\n--- Immutability ---');

    const user = {
        name: 'Alex',
        address: { city: 'Moscow', zip: 101000 }
    };

    // ОШИБКА (Мутация): user.name = 'Ivan';

    // ПРАВИЛЬНО (Иммутабельное обновление):
    const updatedUser = {
        ...user,
        name: 'Ivan',
        address: {
            ...user.address,
            city: 'Saint-P'
        }
    };

    console.log('Original User City:', user.address.city); // Moscow
    console.log('Updated User City:', updatedUser.address.city); // Saint-P
    console.log('Is different object?', user !== updatedUser); // true
};
