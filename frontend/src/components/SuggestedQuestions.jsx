const questions = [
  "What is GitLab's mission?",
  "What are GitLab's values?",
  "What is asynchronous communication at GitLab?",
  "What is GitLab's product direction?",
  "What is GitLab's AI strategy?",
  "What is GitLab's DevSecOps platform direction?",
];

function SuggestedQuestions({ onSelect, disabled }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:p-5 transition dark:border-slate-800 dark:bg-slate-900">
      <p className="mb-3 text-sm font-medium text-slate-600 dark:text-slate-200">Try asking:</p>

      <div className="flex flex-wrap gap-2">
        {questions.map((question) => (
          <button
            key={question}
            onClick={() => onSelect(question)}
            disabled={disabled}
            className="rounded-full border border-slate-300 bg-slate-50 px-4 py-2 text-sm font-medium text-slate-700 transition hover:border-violet-300 hover:bg-violet-200 hover:text-violet-800 active:scale-95 cursor-pointer disabled:cursor-not-allowed disabled:opacity-60"
          >
            {question}
          </button>
        ))}
      </div>
    </div>
  );
}

export default SuggestedQuestions;