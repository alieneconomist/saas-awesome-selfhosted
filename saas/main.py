from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="saas-awesome-selfhosted")

class Request(BaseModel):
    input: str
    options: dict = {}

@app.get("/")
def home():
    return {"name": "saas-awesome-selfhosted", "source": "https://github.com/?/saas-awesome-selfhosted"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "saas-awesome-selfhosted"}

@app.get("/readyz")
def readyz():
    return {"status": "ready", "service": "saas-awesome-selfhosted"}

@app.post("/run")
def run(req: Request):
    """Search this repo's README for matching entries."""
    query = (req.input or "").lower().strip()
    if not query:
        return {"status": "error", "message": "empty query"}
    from pathlib import Path as _P
    readme = _P(__file__).parent.parent / "README.md"
    if not readme.exists():
        # Try lowercase
        for alt in ('readme.md', 'Readme.md', 'awesome.md', 'AWESOME.md'):
            p = _P(__file__).parent.parent / alt
            if p.exists():
                readme = p
                break
    try:
        text = readme.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {"status": "no_data", "message": "README not found"}
    lines = text.splitlines()
    matches = []
    needle = query
    for i, line in enumerate(lines):
        if needle in line.lower() and ("[" in line or "*" in line or "-" in line):
            entry = line.strip()
            if 10 < len(entry) < 400:
                matches.append({"line": i + 1, "entry": entry})
            if len(matches) >= 15:
                break
    return {"status": "ok", "query": req.input, "matches": matches, "total": len(matches)}

@app.get("/suggest")
def suggest():
    """Return popular self-hosted app categories."""
    from pathlib import Path as _P
    readme = _P(__file__).parent.parent / "README.md"
    try:
        text = readme.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {"suggestions": ["media", "photo", "cloud", "git", "chat"]}
    sections = []
    for line in text.splitlines():
        s = line.strip()
        # Self-hosted README uses "## Category" and "### Software"
        if s.startswith("## ") and "Table of Contents" not in s:
            name = s[3:].strip()
            if name and name not in sections and "Sponsors" not in name and len(name) < 50:
                sections.append(name)
    return {"suggestions": sections[:30], "total_sections": len(sections)}


@app.get("/stats")
def stats():
    """Return basic stats about the awesome-selfhosted list."""
    from pathlib import Path as _P
    readme = _P(__file__).parent.parent / "README.md"
    try:
        text = readme.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {"error": "README not found"}
    lines = text.splitlines()
    sections = sum(1 for l in lines if l.startswith("## "))
    links = sum(1 for l in lines if "](" in l)
    return {"lines": len(lines), "sections": sections, "links": links, "size_kb": round(len(text) / 1024, 1)}
