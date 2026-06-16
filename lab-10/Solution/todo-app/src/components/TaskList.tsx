import React from 'react';
import { TodoRecord } from './types';
import { TaskItem } from './TaskItem';

interface TodoListProps {
  records: TodoRecord[];
  onToggle: (taskId: string) => void;
  onDelete: (taskId: string) => void;
}

export function TaskList({ records, onToggle, onDelete }: TodoListProps) {
  if (records.length === 0) {
    return (
      <div className="text-center py-12 bg-neutral-900/50 rounded-xl border border-dashed border-neutral-700">
        <p className="text-neutral-500 text-lg">Задач пока нет</p>
        <p className="text-neutral-600 text-sm mt-2">Добавьте что-нибудь в список!</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {records.map((record) => (
        <TaskItem
          key={record.taskId}
          record={record}
          onToggle={onToggle}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
