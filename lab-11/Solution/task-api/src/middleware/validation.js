const Joi = require('joi');

const taskPostValidation = Joi.object({
  title: Joi.string().min(3).max(120).required().messages({
    'string.min': 'Имя задачи должно содержать хотя бы 3 символа',
    'string.max': 'Имя задачи не должно превышать 120 символов',
    'any.required': 'Имя задачи является обязательным параметром'
  }),
  description: Joi.string().max(600).allow('').messages({
    'string.max': 'Описание не должно превышать 600 символов'
  }),
  category: Joi.string().valid('work', 'study', 'home', 'other').default('other').messages({
    'any.only': 'Допустимые категории задач: work, study, home, other'
  }),
  priority: Joi.number().integer().min(1).max(5).default(3).messages({
    'number.min': 'Ранг важности должен быть от 1 до 5',
    'number.max': 'Ранг важности должен быть от 1 до 5'
  }),
  dueDate: Joi.date().greater('now').messages({
    'date.greater': 'Срок сдачи задачи должен лежать в будущем'
  })
});

const taskPutValidation = Joi.object({
  title: Joi.string().min(3).max(120),
  description: Joi.string().max(600).allow(''),
  category: Joi.string().valid('work', 'study', 'home', 'other'),
  priority: Joi.number().integer().min(1).max(5),
  dueDate: Joi.date().greater('now'),
  completed: Joi.boolean()
});

const verifyTaskInput = (req, res, next) => {
  const { error } = taskPostValidation.validate(req.body, { abortEarly: false });
  if (error) {
    return res.status(400).json({
      error: 'Ошибка верификации параметров',
      details: error.details.map(err => ({
        field: err.path[0],
        message: err.message
      }))
    });
  }
  next();
};

const verifyTaskUpdate = (req, res, next) => {
  const { error } = taskPutValidation.validate(req.body, { abortEarly: false });
  if (error) {
    return res.status(400).json({
      error: 'Ошибка верификации параметров',
      details: error.details.map(err => ({
        field: err.path[0],
        message: err.message
      }))
    });
  }
  if (Object.keys(req.body).length === 0) {
    return res.status(400).json({
      error: 'Ошибка верификации параметров',
      message: 'Запрос на изменение должен содержать как минимум одно обновляемое поле'
    });
  }
  next();
};

const verifyTaskIdParam = (req, res, next) => {
  const taskId = parseInt(req.params.id, 10);
  if (isNaN(taskId) || taskId <= 0) {
    return res.status(400).json({
      error: 'Ошибка верификации параметров',
      message: 'Идентификатор задачи должен представлять собой целое положительное число'
    });
  }
  req.params.id = taskId;
  next();
};

module.exports = {
  verifyTaskInput,
  verifyTaskUpdate,
  verifyTaskIdParam
};
