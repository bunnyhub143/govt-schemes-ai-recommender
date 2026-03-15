"""
Load and search government scheme data from india_government_schemes_dataset.csv.
Columns: Category, Scheme Name, Description, Official Link
"""
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILES = [
    BASE_DIR / "india_government_schemes_dataset.csv",
    BASE_DIR / "additional_india_government_schemes.csv",
    BASE_DIR / "latest_government_schemes_2026.csv",
    BASE_DIR / "india_government_schemes.csv",
    BASE_DIR / "india_government_schemes2026.csv",
]

_cache = None


def _load_schemes():
    """Load all schemes from the CSV file (cached)."""
    global _cache
    if _cache is not None:
        return _cache

    schemes = []
    idx = 0
    for csv_file in CSV_FILES:
        try:
            with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = (row.get("Scheme Name") or "").strip()
                    if not name:
                        continue
                    schemes.append({
                        "id": idx,
                        "name": name,
                        "category": (row.get("Category") or "Other").strip(),
                        "description": (row.get("Description") or "").strip(),
                        "website": (row.get("Official Link") or "").strip(),
                    })
                    idx += 1
        except Exception as e:
            print(f"Error loading {csv_file}: {e}")

    _cache = schemes
    return schemes


def get_all_categories():
    """Return all categories with their scheme counts."""
    schemes = _load_schemes()
    cat_counts = {}
    for s in schemes:
        cat = s["category"]
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    return sorted(cat_counts.items(), key=lambda x: -x[1])


def get_schemes_by_category(category):
    """Return all schemes matching a given category."""
    schemes = _load_schemes()
    if category == "All":
        return schemes
    return [s for s in schemes if s["category"] == category]


def get_all_schemes():
    """Return all schemes."""
    return _load_schemes()


def search_schemes(query):
    """Search schemes by keyword."""
    query_lower = query.lower().strip()
    if not query_lower:
        return []
    results = []
    for s in _load_schemes():
        text = (s["name"] + " " + s["description"] + " " + s["category"]).lower()
        if query_lower in text:
            results.append(s)
    return results


def recommend_schemes(user):
    """AI-based scheme recommendation based on user profile."""
    if not user:
        return []

    age = user.age
    income = user.income
    occupation = (user.occupation or "").lower()

    scored = []

    for scheme in _load_schemes():
        text = (scheme["name"] + " " + scheme["description"]).lower()
        cat = scheme["category"].lower()
        score = 0

        # Age-based scoring
        if age:
            if age < 18 and any(w in text for w in ["child", "student", "school", "girl", "beti", "vidya"]):
                score += 3
            elif 18 <= age <= 25 and any(w in text for w in ["student", "youth", "scholarship", "education", "skill", "employment"]):
                score += 3
            elif 25 < age <= 60 and any(w in text for w in ["employment", "loan", "farmer", "worker", "business", "enterprise", "skill"]):
                score += 2
            elif age > 60 and any(w in text for w in ["pension", "senior", "old age", "elderly"]):
                score += 4

        # Income-based scoring
        if income is not None:
            if income < 100000 and any(w in text for w in ["bpl", "poor", "low income", "free", "subsidy", "below poverty"]):
                score += 3
            elif income < 300000 and any(w in text for w in ["subsidy", "loan", "affordable", "assistance", "benefit"]):
                score += 2
            elif income < 500000 and any(w in text for w in ["credit", "loan", "insurance"]):
                score += 1

        # Occupation-based scoring
        if occupation:
            occ_map = {
                "farmer": ["farmer", "kisan", "agriculture", "crop", "irrigation", "krishi", "agricultural"],
                "student": ["student", "scholarship", "education", "school", "college", "vidya"],
                "business": ["business", "enterprise", "mudra", "startup", "msme", "vendor", "loan", "entrepreneur"],
                "worker": ["worker", "labour", "employment", "skill", "rozgar", "construction", "unorganised"],
                "teacher": ["education", "teacher", "school", "training"],
                "doctor": ["health", "medical", "hospital"],
                "unemployed": ["employment", "skill", "rozgar", "job", "training", "livelihood"],
                "housewife": ["women", "mahila", "self help", "maternity", "girl"],
            }
            for occ_key, occ_keywords in occ_map.items():
                if occ_key in occupation:
                    for kw in occ_keywords:
                        if kw in text:
                            score += 2
                            break

        # Category-based bonus for occupation
        if occupation:
            if "farmer" in occupation and "agriculture" in cat:
                score += 3
            if "student" in occupation and "education" in cat:
                score += 3
            if any(w in occupation for w in ["business", "entrepreneur"]) and "enterprise" in cat:
                score += 3
            if any(w in occupation for w in ["housewife", "woman"]) and "women" in cat:
                score += 3

        if score > 0:
            scored.append((score, scheme))

    # Sort by score descending and return top 20
    scored.sort(key=lambda x: -x[0])
    return [s for _, s in scored[:20]]
