"""
Main blueprint: dashboard, profile, schemes, AI recommender.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from app.schemes import (
    get_all_categories, get_schemes_by_category,
    get_all_schemes, recommend_schemes, search_schemes,
)

main_bp = Blueprint("main", __name__)


@main_bp.route("/dashboard")
@login_required
def dashboard():
    recommended = []
    if not current_user.get_id().startswith("admin:"):
        recommended = recommend_schemes(current_user)[:6]
    categories = get_all_categories()
    total = len(get_all_schemes())
    return render_template(
        "dashboard.html",
        recommended=recommended,
        categories=categories,
        total_schemes=total,
    )


@main_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if current_user.get_id().startswith("admin:"):
        flash("Admins do not have a profile page.", "info")
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        age = request.form.get("age")
        occupation = (request.form.get("occupation") or "").strip()
        income = request.form.get("income")

        try:
            current_user.age = int(age) if age else None
        except ValueError:
            current_user.age = None
        current_user.occupation = occupation or None
        try:
            current_user.income = float(income) if income else None
        except ValueError:
            current_user.income = None

        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("main.profile"))

    return render_template("profile.html")


@main_bp.route("/schemes")
@login_required
def schemes_browse():
    categories = get_all_categories()
    return render_template("schemes_browse.html", categories=categories)


@main_bp.route("/schemes/category/<category>")
@login_required
def schemes_by_cat(category):
    schemes = get_schemes_by_category(category)
    return render_template(
        "schemes_list.html",
        schemes=schemes,
        title=f"Category: {category}",
        subtitle=f"{len(schemes)} schemes found",
    )


@main_bp.route("/schemes/all")
@login_required
def schemes_all():
    schemes = get_all_schemes()
    return render_template(
        "schemes_list.html",
        schemes=schemes,
        title="All Schemes",
        subtitle=f"{len(schemes)} schemes in total",
    )


@main_bp.route("/schemes/search")
@login_required
def schemes_search():
    q = request.args.get("q", "").strip()
    results = search_schemes(q) if q else []
    return render_template(
        "schemes_list.html",
        schemes=results,
        title=f'Search: "{q}"' if q else "Search Schemes",
        subtitle=f"{len(results)} results" if q else "Enter a keyword to search",
        query=q,
    )


@main_bp.route("/recommend")
@login_required
def recommend():
    if current_user.get_id().startswith("admin:"):
        flash("AI Recommender is for registered users only.", "info")
        return redirect(url_for("main.dashboard"))

    schemes = recommend_schemes(current_user)
    has_profile = bool(current_user.age or current_user.income or current_user.occupation)
    return render_template(
        "recommend.html",
        schemes=schemes,
        has_profile=has_profile,
    )
