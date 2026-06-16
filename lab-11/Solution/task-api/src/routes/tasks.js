const express = require('express');
const router = express.Router();
const { v4: uuidv4 } = require('uuid');
const { verifyTaskInput, verifyTaskUpdate, verifyTaskIdParam } = require('../middleware/validation');
const { initializeDataFile, readData, writeData, getNextId } = require('../utils/fileOperations');

initializeDataFile();

// Извлечение всего списка задач по фильтрам
router.get('/', async (req, res, next) => {
  try {
    const { category, completed, priority, sortBy, page, limit, q } = req.query;
    const store = await readData();
    let currentList = [...store.tasks];
    
    if (category) {
      currentList = currentList.filter(t => t.category === category);
    }
    if (completed !== undefined) {
      currentList = currentList.filter(t => t.completed === (completed === 'true'));
    }
    if (priority) {
      currentList = currentList.filter(t => t.priority === parseInt(priority, 10));
    }
    if (q && q.trim().length >= 2) {
      const searchStr = q.toLowerCase().trim();
      currentList = currentList.filter(t => 
        t.title.toLowerCase().includes(searchStr) || 
        (t.description && t.description.toLowerCase().includes(searchStr))
      );
    }
    
    if (sortBy) {
      const isReverse = sortBy.startsWith('-');
      const targetField = isReverse ? sortBy.slice(1) : sortBy;
      currentList.sort((x, y) => {
        let a = x[targetField], b = y[targetField];
        if (targetField === 'dueDate' || targetField === 'createdAt') {
          a = a ? new Date(a).getTime() : 0;
          b = b ? new Date(b).getTime() : 0;
        }
        if (a < b) return isReverse ? 1 : -1;
        if (a > b) return isReverse ? -1 : 1;
        return 0;
      });
    }
    
    let slicedResult = currentList;
    if (page && limit) {
      const pageIdx = parseInt(page, 10);
      const limitVal = parseInt(limit, 10);
      slicedResult = currentList.slice((pageIdx - 1) * limitVal, pageIdx * limitVal);
    }
    
    res.json({ 
      success: true, 
      count: slicedResult.length, 
      total: currentList.length, 
      data: slicedResult 
    });
  } catch (err) { 
    next(err); 
  }
});

// Текстовый поиск по свойствам задач
router.get('/search/text', async (req, res, next) => {
  try {
    const { q } = req.query;
    if (!q || q.trim().length < 2) {
      return res.status(400).json({ 
        success: false, 
        error: 'Строка поиска должна быть длиннее 1 символа' 
      });
    }
    const store = await readData();
    const queryTerm = q.toLowerCase().trim();
    const found = store.tasks.filter(t => 
      t.title.toLowerCase().includes(queryTerm) || 
      (t.description && t.description.toLowerCase().includes(queryTerm))
    );
    res.json({ success: true, count: found.length, data: found });
  } catch (err) { 
    next(err); 
  }
});

// Расчет аналитической сводки
router.get('/stats/summary', async (req, res, next) => {
  try {
    const store = await readData();
    const list = store.tasks;
    const statistics = { 
      total: list.length, 
      completed: 0, 
      pending: 0, 
      overdue: 0, 
      byCategory: {}, 
      byPriority: { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 } 
    };
    const dateNow = new Date();
    
    list.forEach(t => {
      if (t.completed) {
        statistics.completed++;
      } else {
        statistics.pending++;
        if (t.dueDate && new Date(t.dueDate) < dateNow) {
          statistics.overdue++;
        }
      }
      statistics.byCategory[t.category] = (statistics.byCategory[t.category] || 0) + 1;
      if (t.priority >= 1 && t.priority <= 5) {
        statistics.byPriority[t.priority]++;
      }
    });
    
    res.json({ success: true, data: statistics });
  } catch (err) { 
    next(err); 
  }
});

// Получение одной задачи по ID
router.get('/:id', verifyTaskIdParam, async (req, res, next) => {
  try {
    const store = await readData();
    const result = store.tasks.find(t => t.id === req.params.id);
    if (!result) { 
      const err = new Error('Искомая задача не найдена'); 
      err.status = 404; 
      throw err; 
    }
    res.json({ success: true, data: result });
  } catch (err) { 
    next(err); 
  }
});

// Добавление новой задачи
router.post('/', verifyTaskInput, async (req, res, next) => {
  try {
    const { title, description, category, priority, dueDate } = req.body;
    const store = await readData();
    const record = {
      id: await getNextId(), 
      uuid: uuidv4(), 
      title, 
      description: description || '',
      category: category || 'other', 
      priority: priority || 3, 
      dueDate: dueDate || null,
      completed: false, 
      createdAt: new Date().toISOString(), 
      updatedAt: new Date().toISOString()
    };
    store.tasks.push(record);
    await writeData(store);
    res.status(201).json({ 
      success: true, 
      message: 'Задача добавлена в очередь', 
      data: record 
    });
  } catch (err) { 
    next(err); 
  }
});

// Обновление полей задачи по ID
router.put('/:id', verifyTaskIdParam, verifyTaskUpdate, async (req, res, next) => {
  try {
    const fieldsToChange = req.body;
    const store = await readData();
    const idx = store.tasks.findIndex(t => t.id === req.params.id);
    if (idx === -1) { 
      const err = new Error('Редактируемый объект отсутствует'); 
      err.status = 404; 
      throw err; 
    }
    const updated = { 
      ...store.tasks[idx], 
      ...fieldsToChange, 
      updatedAt: new Date().toISOString() 
    };
    store.tasks[idx] = updated;
    await writeData(store);
    res.json({ 
      success: true, 
      message: 'Параметры задачи обновлены в базе', 
      data: updated 
    });
  } catch (err) { 
    next(err); 
  }
});

// Закрытие задачи (complete) по ID
router.patch('/:id/complete', verifyTaskIdParam, async (req, res, next) => {
  try {
    const store = await readData();
    const idx = store.tasks.findIndex(t => t.id === req.params.id);
    if (idx === -1) { 
      const err = new Error('Искомая задача отсутствует'); 
      err.status = 404; 
      throw err; 
    }
    store.tasks[idx].completed = true;
    store.tasks[idx].updatedAt = new Date().toISOString();
    await writeData(store);
    res.json({ 
      success: true, 
      message: 'Задача помечена как выполненная', 
      data: store.tasks[idx] 
    });
  } catch (err) { 
    next(err); 
  }
});

// Удаление задачи из системы по ID
router.delete('/:id', verifyTaskIdParam, async (req, res, next) => {
  try {
    const store = await readData();
    const idx = store.tasks.findIndex(t => t.id === req.params.id);
    if (idx === -1) { 
      const err = new Error('Удаляемая задача не найдена'); 
      err.status = 404; 
      throw err; 
    }
    store.tasks.splice(idx, 1);
    await writeData(store);
    res.json({ success: true, message: 'Задача успешно стерта из базы' });
  } catch (err) { 
    next(err); 
  }
});

module.exports = router;
