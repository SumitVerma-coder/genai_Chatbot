GITLAB_KEYWORDS = [
    "gitlab",
    "handbook",
    "direction",
    "directions",
    "remote",
    "all remote",
    "values",
    "mission",
    "teamops",
    "merge request",
    "merge requests",
    "devops",
    "devsecops",
    "ci/cd",
    "company",
    "culture",
    "employee",
    "engineering",
    "product",
    "security",
    "sales",
    "marketing",
    "support",
    "people group",
    "dri",
    "directly responsible individual",
    "asynchronous",
    "async",
    "handbook-first",
    "handbook first",
    "transparency",
    "iteration",
    "collaboration",
    "roadmap",
    "strategy",
    "platform",
    "workflow",
]


FOLLOW_UP_KEYWORDS = [
    "it",
    "this",
    "that",
    "they",
    "them",
    "those",
    "these",
    "explain",
    "summarize",
    "simplify",
    "simple",
    "short",
    "brief",
    "more",
    "details",
    "example",
    "examples",
    "why",
    "how",
    "compare",
    "difference",
    "elaborate",
]


def is_gitlab_related(question: str) -> bool:
    question = question.lower()

    return any(keyword in question for keyword in GITLAB_KEYWORDS)


def is_possible_followup(question: str) -> bool:
    question = question.lower()

    return any(keyword in question for keyword in FOLLOW_UP_KEYWORDS)