import React from 'react';
import { TodoRecord } from './types';

interface TodoStatsProps {
  records: TodoRecord[];
}

export function TaskStats({ records }: TodoStatsProps) {
  const totalItems = records.length;
  const doneItems = records.filter(r => r.isCompleted).length;
  const completionRate = totalItems === 0 ? 0 : Math.round((doneItems / totalItems) * 100);

  return (
    <div className="mt-8 pt-6 border-t border-neutral-700">
      <div className="flex justify-between items-center mb-2">
        <p className="text-neutral-400 font-medium">Статистика задач:</p>
        <p className="text-amber-500 font-bold">{doneItems} из {totalItems}</p>
      </div>
      
      {/* Прогресс-бар (Янтарный на темном) */}
      <div className="w-full bg-neutral-800 rounded-full h-2.5 mb-2 overflow-hidden">
        <div 
          className="bg-amber-500 h-2.5 rounded-full transition-all duration-500" 
          style={{ width: `${completionRate}%` }}
        ></div>
      </div>
      <p className="text-xs text-neutral-500 text-right">{completionRate}% выполнено</p>
    </div>
  );
}
