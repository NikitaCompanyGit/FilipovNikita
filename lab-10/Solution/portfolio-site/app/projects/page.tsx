import ProjectCard from '../components/ProjectCard'

const projectList = [
  {
    title: 'Library catalog REST API',
    description: 'Асинхронный REST API на FastAPI для инвентаризации книг в библиотеке. Включает гибкую фильтрацию, валидацию Pydantic и Swagger документацию.',
    stack: ['Python', 'FastAPI', 'Pydantic', 'SQLite'],
    repoUrl: 'https://github.com/filipov/library-rest-api'
  },
  {
    title: 'Task Management Backend',
    description: 'Веб-служба для ведения и распределения задач. Реализована на Express.js с валидацией Joi и поддержкой полнотекстового поиска.',
    stack: ['Node.js', 'Express', 'Joi', 'File System'],
    repoUrl: 'https://github.com/filipov/task-manager-backend'
  },
  {
    title: 'News Aggregator WebApp',
    description: 'PWA-приложение для агрегации новостей с оффлайн-режимом работы, реализованным через Service Workers и IndexedDB.',
    stack: ['JavaScript', 'IndexedDB', 'Service Workers', 'HTML5/CSS3'],
    linkUrl: 'https://news-aggregator-pwa.example.com'
  }
];

export default function ProjectsPage() {
  return (
    <div className="max-w-6xl mx-auto py-4">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-extrabold text-slate-100 mb-4 tracking-tight">Мои Проекты</h1>
        <p className="text-lg text-slate-400 max-w-2xl mx-auto">
          Каталог разработанных решений, демонстрирующих практический опыт в веб-разработке и системной архитектуре.
        </p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {projectList.map((proj, index) => (
          <ProjectCard 
            key={index}
            title={proj.title}
            description={proj.description}
            stack={proj.stack}
            linkUrl={proj.linkUrl}
            repoUrl={proj.repoUrl}
          />
        ))}
      </div>
    </div>
  )
}
