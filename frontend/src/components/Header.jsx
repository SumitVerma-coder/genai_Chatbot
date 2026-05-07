function Header() {
  return (
    <header className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6 transition dark:border-slate-800 dark:bg-slate-900">
      <div className="flex flex-col gap-2">

        <h1 className="text-3xl font-bold tracking-tight text-violet-600 sm:text-4xl  dark:text-slate-200">
          GitLab Handbook Chatbot
        </h1>

        <p className="max-w-2xl text-sm leading-6 text-slate-600 sm:text-base dark:text-slate-100">
          Your helping hand for questions related to Gitlab.
        </p>
      </div>
    </header>
  );
}

export default Header;