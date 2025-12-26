// src/react-concepts.js
// ВНИМАНИЕ: Этот код предназначен для среды React, не для Node.js

import React, { useState, useMemo } from 'react';

export const ProductList = ({ products }) => {
    const [filter, setFilter] = useState('');

    // useMemo - мемоизация тяжелых вычислений (аналог кэширования)
    const visibleProducts = useMemo(() => {
        console.log('Filtering...');
        return products.filter(p => p.name.includes(filter));
    }, [products, filter]);

    return (
        <div>
            <input onChange={e => setFilter(e.target.value)} />
            {visibleProducts.map(p => <div key={p.id}>{p.name}</div>)}
        </div>
    );
};
