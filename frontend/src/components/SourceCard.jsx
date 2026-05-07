function SourceCard({ source }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-3 shadow-sm">
      <h4 className="text-sm font-semibold text-slate-900">
        {source.title}
      </h4>

      {source.snippet && (
        <p className="mt-2 text-sm leading-5 text-slate-600">
          {source.snippet}
        </p>
      )}

      {source.url && (
        <a
          href={source.url}
          target="_blank"
          rel="noreferrer"
          className="mt-2 inline-block text-sm font-semibold text-violet-600 transition hover:text-violet-700"
        >
          View source
        </a>
      )}
    </div>
  );
}

export default SourceCard;