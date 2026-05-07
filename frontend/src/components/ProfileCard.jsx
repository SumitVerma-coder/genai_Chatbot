function ProfileCard({ user }) {
  return (
    <div className="rounded-2xl bg-violet-50 p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-violet-600">
        Profile
      </p>

      <div className="mt-3 flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-violet-600 text-sm font-bold text-white">
          {user?.name?.charAt(0)?.toUpperCase() || "U"}
        </div>

        <div className="min-w-0">
          <h2 className="truncate font-bold text-slate-900">
            {user?.name || "User"}
          </h2>
          <p className="truncate text-sm text-slate-600">
            {user?.email || "No email"}
          </p>
        </div>
      </div>
    </div>
  );
}

export default ProfileCard;