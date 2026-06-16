# **Лабораторная работа 1. Часть 1: React-приложение с Vite**

## **Тема:** Создание простого веб-интерфейса на современном стеке

### **Цель работы:**
Практическое знакомство с созданием React-приложений с использованием TypeScript и Vite. Освоение базовых концепций компонентного подхода и состояния.

---

## **Задание: Управление списком задач (To-Do List)**

Разработайте простое React-приложение для управления списком задач.

### **1. Настройка проекта**

Откройте терминал в Ubuntu и выполните:

```bash
# Создание проекта с помощью Vite
npm create vite@latest todo-app -- --template react-ts
cd todo-app

# Установка зависимостей
npm install

# Установка Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Настройте Tailwind CSS в `tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Добавьте в `src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### **2. Базовый интерфейс приложения**

**Файл: `src/App.tsx`**

```tsx
import React, { useState } from 'react';

// Тип для задачи
interface Task {
  id: number;
  text: string;
  completed: boolean;
}

function App() {
  // Состояние для списка задач
  const [tasks, setTasks] = useState<Task[]>([
    { id: 1, text: 'Изучить React', completed: true },
    { id: 2, text: 'Написать To-Do приложение', completed: false }
  ]);

  // Состояние для новой задачи
  const [newTask, setNewTask] = useState('');

  // Функция добавления задачи
  const addTask = () => {
    if (newTask.trim() === '') return;
    
    const task: Task = {
      id: Date.now(),
      text: newTask,
      completed: false
    };
    
    setTasks([...tasks, task]);
    setNewTask('');
  };

  // Функция удаления задачи (ДОПОЛНИТЕ САМОСТОЯТЕЛЬНО)
  const removeTask = (id: number) => {
    // TODO: Реализуйте удаление задачи по ID
    // Подсказка: используйте метод filter для создания нового массива
  };

  // Функция переключения статуса задачи (ДОПОЛНИТЕ САМОСТОЯТЕЛЬНО)
  const toggleTask = (id: number) => {
    // TODO: Реализуйте переключение статуса completed
    // Подсказка: используйте метод map для обновления массива
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-6">
        <h1 className="text-3xl font-bold text-center mb-6 text-gray-800">
          📝 Список задач
        </h1>
        
        {/* Форма добавления задачи */}
        <div className="flex gap-2 mb-6">
          <input
            type="text"
            value={newTask}
            onChange={(e) => setNewTask(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && addTask()}
            placeholder="Введите новую задачу..."
            className="flex-grow px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={addTask}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
          >
            Добавить
          </button>
        </div>

        {/* Список задач */}
        <div className="space-y-3">
          {tasks.map(task => (
            <div 
              key={task.id} 
              className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border"
            >
              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => toggleTask(task.id)}
                  className="h-5 w-5 text-blue-600"
                />
                <span className={`${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                  {task.text}
                </span>
              </div>
              
              {/* Кнопка удаления (ДОПОЛНИТЕ САМОСТОЯТЕЛЬНО) */}
              <button
                onClick={() => removeTask(task.id)}
                className="text-red-500 hover:text-red-700"
              >
                {/* TODO: Добавьте иконку удаления или текст "Удалить" */}
              </button>
            </div>
          ))}
        </div>

        {/* Статистика (ДОПОЛНИТЕ САМОСТОЯТЕЛЬНО) */}
        <div className="mt-6 pt-4 border-t">
          <p className="text-gray-600">
            Всего задач: {tasks.length}
          </p>
          {/* TODO: Добавьте отображение количества выполненных задач */}
        </div>
      </div>
    </div>
  );
}

export default App;
```

### **3. Задания для самостоятельного выполнения**

#### **Основные задачи (обязательные):**

**A. Реализуйте функцию удаления задач**

Дополните функцию `removeTask` в `App.tsx`. Ваша реализация должна:
- Удалять задачу по её уникальному ID
- Использовать неизменяемый подход (не мутировать исходный массив)
- Создавать новый массив без удаляемой задачи

```typescript
const removeTask = (id: number) => {
  // Реализуйте удаление задачи по ID
  // Используйте метод filter для создания нового массива
};
```

**B. Реализуйте переключение статуса задачи**

Дополните функцию `toggleTask`. Ваша реализация должна:
- Находить задачу по ID
- Инвертировать её статус выполнения (completed)
- Сохранять неизменяемость состояния

```typescript
const toggleTask = (id: number) => {
  // Реализуйте переключение статуса completed
  // Используйте метод map для обновления массива задач
};
```

**C. Добавьте кнопку удаления**

В блоке кнопки удаления добавьте визуальный элемент:
- Текст "Удалить" или иконку (например, × или корзину)
- Стилизуйте кнопку для лучшего UX

```tsx
<button
  onClick={() => removeTask(task.id)}
  className="px-3 py-1 text-red-500 hover:text-red-700 hover:bg-red-50 rounded"
>
  {/* Добавьте текст "Удалить" или иконку × */}
</button>
```

#### **Дополнительные задачи (по желанию):**

**D. Добавьте отображение статистики**

В блоке статистики реализуйте:
- Подсчёт количества выполненных задач
- Отображение прогресса выполнения

```tsx
<p className="text-gray-600">
  Выполнено: {/* Посчитайте количество выполненных задач */}
</p>
```

**E. Добавьте компонент для пустого списка**

Реализуйте условный рендеринг:
- Если список задач пуст, показывайте информационное сообщение
- Добавьте призыв к действию

```tsx
{/* После map */}
{tasks.length === 0 && (
  <div className="text-center py-8 text-gray-500">
    <p>Список задач пуст</p>
    <p className="text-sm">Добавьте первую задачу!</p>
  </div>
)}
```

### **4. Запуск и проверка**

```bash
# Запуск в режиме разработки
npm run dev

# Сборка проекта
npm run build

# Превью собранного проекта
npm run preview
```

Откройте браузер и перейдите по адресу: `http://localhost:5173`

### **5. Что должно быть в отчёте:**

1. **Исходный код:**
   - Полный код файла `App.tsx` с вашими дополнениями
   - Комментарии к реализованным функциям

2. **Скриншоты работающего приложения:**
   - Главный экран с задачами
   - Добавление новой задачи
   - Задача в состоянии "выполнено"
   - Удаление задачи

3. **Ответы на вопросы:**
   - Объясните принцип работы хука `useState`
   - Почему в React важно использовать неизменяемое состояние?
   - Какой метод массива вы использовали для удаления задачи и почему?
   - В чём преимущества TypeScript при разработке React-приложений?

### **6. Критерии оценивания:**

#### **Обязательные требования:**
- **Функция удаления задач:** Реализована корректно, использует метод `filter`, не мутирует исходный массив
- **Функция переключения статуса:** Корректно инвертирует статус выполнения, использует метод `map`, сохраняет неизменяемость
- **Кнопка удаления:** Имеет понятный визуальный элемент (текст/иконку), стилизована для улучшения UX
- **Приложение запускается:** Нет ошибок компиляции, интерфейс отображается корректно

#### **Дополнительные критерии (для повышения оценки):**
- **Статистика задач:** Реализован подсчёт и отображение выполненных задач
- **Обработка пустого списка:** Есть информационное сообщение при отсутствии задач
- **Качество кода:** Чистый, читаемый код с комментариями, правильное именование переменных
- **Дополнительный функционал:** Любые улучшения сверх требований задания

#### **Неприемлемые ошибки:**
- Мутация состояния напрямую (например, `tasks.push()`)
- Ошибки TypeScript-типизации
- Критические ошибки в работе приложения
- Отсутствие ключей (key) при рендеринге списка

### **7. Полезные команды для Ubuntu:**

```bash
# Проверка установленных версий
node --version
npm --version

# Если Node.js не установлен
sudo apt update
sudo apt install nodejs npm

# Установка последней версии npm
sudo npm install -g npm@latest
```

### **8. Структура проекта:**

```
todo-app/
├── src/
│   ├── App.tsx          # Основной компонент приложения
│   ├── main.tsx         # Точка входа
│   └── index.css        # Глобальные стили с Tailwind
├── public/              # Статические файлы
├── index.html           # HTML шаблон
├── package.json         # Зависимости и скрипты
├── tailwind.config.js   # Конфигурация Tailwind
├── vite.config.ts       # Конфигурация Vite
└── tsconfig.json        # Конфигурация TypeScript
```

### **9. Советы по выполнению:**

1. **Сначала запустите** предоставленный код без изменений
2. **Постепенно дополняйте** функции по одной
3. **Проверяйте результат** после каждого изменения
4. **Используйте консоль разработчика** в браузере для отладки
5. **Читайте сообщения об ошибках** — они часто подсказывают решение

**Примечание:** В задании предоставлено ~70% кода. Ваша задача — понять логику работы и дописать недостающие ~30%, следуя принципам React и TypeScript.
