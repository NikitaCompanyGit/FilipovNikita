import React from 'react';
import { TodoRecord } from './types';

interface TodoItemProps {
  record: TodoRecord;
  onToggle: (taskId: string) => void;
  onDelete: (taskId: string) => void;
}

export function TaskItem({ record, onToggle, onDelete }: TodoItemProps) {
  return (
    <div className="flex items-center justify-between p-4 bg-neutral-900 rounded-xl border border-neutral-800 shadow-sm hover:border-neutral-700 transition-all group">
      <div className="flex items-center gap-4 flex-grow">
        <label className="relative flex items-center cursor-pointer">
          <input
            type="checkbox"
            checked={record.isCompleted}
            onChange={() => onToggle(record.taskId)}
            className="peer sr-only"
          />
          <div className="w-6 h-6 border-2 border-neutral-600 rounded-md peer-checked:bg-amber-500 peer-checked:border-amber-500 transition-all flex items-center justify-center bg-neutral-800">
            {record.isCompleted && (
              <svg className="w-4 h-4 text-neutral-950" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3.5} d="M5 13l4 4L19 7" />
              </svg>
            )}
          </div>
        </label>
        <span className={`text-lg transition-all duration-300 ${record.isCompleted ? 'line-through text-neutral-600' : 'text-neutral-200'}`}>
          {record.textValue}
        </span>
      </div>
      <button
        onClick={() => onDelete(record.taskId)}
        className="opacity-0 group-hover:opacity-100 p-2 text-rose-500 hover:text-rose-400 hover:bg-neutral-800 rounded-lg transition-all"
        aria-label="Удалить"
        title="Удалить задачу"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
      </button>
    </div>
  );
}
