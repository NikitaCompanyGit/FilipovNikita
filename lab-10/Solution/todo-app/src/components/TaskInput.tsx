import React, { useState } from 'react';

interface TodoInputProps {
  onAdd: (text: string) => void;
}

export function TaskInput({ onAdd }: TodoInputProps) {
  const [value, setValue] = useState('');

  const handleSubmit = () => {
    if (value.trim()) {
      onAdd(value.trim());
      setValue('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSubmit();
    }
  };

  return (
    <div className="flex gap-3 mb-8">
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Добавить новую задачу..."
        className="flex-grow px-5 py-3 text-lg bg-neutral-900 border border-neutral-700 rounded-xl text-neutral-200 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500 transition-all shadow-sm"
      />
      <button
        onClick={handleSubmit}
        className="px-6 py-3 bg-amber-500 text-neutral-950 font-bold rounded-xl hover:bg-amber-600 active:scale-95 transition-all shadow-md"
      >
        Добавить
      </button>
    </div>
  );
}
