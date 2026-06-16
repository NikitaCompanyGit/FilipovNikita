import type { Metadata } from 'next'
import { Montserrat } from 'next/font/google'
import './globals.css'

const montserrat = Montserrat({ 
  subsets: ['cyrillic', 'latin'],
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'FilipovDev | Пространство Разработчика',
  description: 'Личный сайт-портфолио и блог Никиты Филиппова, посвященный инженерии ПО',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ru">
      <body className={`${montserrat.className} bg-slate-900 text-slate-100 min-h-screen flex flex-col`}>
        <header className="bg-slate-950 text-white shadow-md sticky top-0 z-50 border-b border-slate-800">
          <nav className="container mx-auto px-6 py-4 flex justify-between items-center">
            <div className="text-xl font-black tracking-wider text-violet-400">
              <a href="/" className="hover:text-violet-300 transition-colors">FILIPOV.DEV</a>
            </div>
            <ul className="flex space-x-6 text-sm font-semibold uppercase tracking-widest">
              <li><a href="/" className="hover:text-violet-400 transition-colors">Главная</a></li>
              <li><a href="/about" className="hover:text-violet-400 transition-colors">Обо мне</a></li>
              <li><a href="/blog" className="hover:text-violet-400 transition-colors">Блог</a></li>
              <li><a href="/projects" className="hover:text-violet-400 transition-colors">Проекты</a></li>
            </ul>
          </nav>
        </header>
        <main className="container mx-auto px-6 py-10 flex-grow">
          {children}
        </main>
        <footer className="bg-slate-950 text-slate-500 py-8 text-center text-sm border-t border-slate-900 mt-auto">
          <p>© {new Date().getFullYear()} FilipovDev. Создано с применением Next.js App Router.</p>
        </footer>
      </body>
    </html>
  )
}
