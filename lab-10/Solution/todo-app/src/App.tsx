import React, { useState } from 'react';
import { TodoRecord } from './components/types';
import { TaskInput } from './components/TaskInput';
import { TaskList } from './components/TaskList';
import { TaskStats } from './components/TaskStats';

function App() {
  const [items, setItems] = useState<TodoRecord[]>([
    { taskId: 'task-1', textValue: 'Разобраться с жизненным циклом компонентов', isCompleted: true },
    { taskId: 'task-2', textValue: 'Сделать рефакторинг лабы 10', isCompleted: false },
    { taskId: 'task-3', textValue: 'Подготовить отчет о выполнении', isCompleted: false },
  ]);

  // Добавление
  const handleInsertTodo = (text: string) => {
    const newRecord: TodoRecord = {
      taskId: crypto.randomUUID(),
      textValue: text,
      isCompleted: false,
    };
    setItems([...items, newRecord]);
  };

  // Удаление
  const handleRemoveTodo = (taskId: string) => {
    setItems(items.filter((item) => item.taskId !== taskId));
  };

  // Переключение состояния
  const handleToggleTodo = (taskId: string) => {
    setItems(
      items.map((item) =>
        item.taskId === taskId ? { ...item, isCompleted: !item.isCompleted } : item
      )
    );
  };

  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-100 py-12 px-4 sm:px-6 lg:px-8 font-sans">
      <div className="max-w-2xl mx-auto bg-neutral-900 border border-neutral-800 rounded-3xl shadow-2xl p-6 md:p-8">
        <h1 className="text-3xl font-extrabold text-center mb-8 text-transparent bg-clip-text bg-gradient-to-r from-amber-400 to-orange-500">
          ⚡ Мой Органайзер
        </h1>

        <TaskInput onAdd={handleInsertTodo} />
        
        <TaskList 
          records={items} 
          onToggle={handleToggleTodo} 
          onDelete={handleRemoveTodo} 
        />
        
        <TaskStats records={items} />
      </div>
    </div>
  );
}

export default App;
