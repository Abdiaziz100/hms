from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from db import get_db
from security import roles_required, login_required
import sqlite3

bp = Blueprint("departments", __name__, url_prefix="/departments")


@bp.route("/")
@login_required
def index():
    rows = get_db().execute(
        "SELECT dep.*, (SELECT COUNT(*) FROM doctors d WHERE d.department_id=dep.id) AS doctor_count "
        "FROM departments dep ORDER BY dep.name").fetchall()
    return render_template("departments/list.html", rows=rows)


@bp.route("/new", methods=["GET", "POST"])
@roles_required("admin")
def create():
    if request.method == "POST":
        name, desc = request.form.get("name", "").strip(), request.form.get("description", "").strip()
        if not name:
            flash("Department name is required.", "danger")
        else:
            try:
                db = get_db()
                db.execute("INSERT INTO departments (name, description) VALUES (?,?)", (name, desc))
                db.commit()
                flash("Department added.", "success")
                return redirect(url_for("departments.index"))
            except sqlite3.IntegrityError:
                flash("A department with that name already exists.", "danger")
    return render_template("departments/form.html", d={"name": "", "description": ""}, editing=False)


@bp.route("/<int:did>/edit", methods=["GET", "POST"])
@roles_required("admin")
def edit(did):
    db = get_db()
    d = db.execute("SELECT * FROM departments WHERE id=?", (did,)).fetchone()
    if not d:
        abort(404)
    if request.method == "POST":
        name, desc = request.form.get("name", "").strip(), request.form.get("description", "").strip()
        if not name:
            flash("Department name is required.", "danger")
        else:
            try:
                db.execute("UPDATE departments SET name=?, description=? WHERE id=?", (name, desc, did))
                db.commit()
                flash("Department updated.", "success")
                return redirect(url_for("departments.index"))
            except sqlite3.IntegrityError:
                flash("A department with that name already exists.", "danger")
        d = {"id": did, "name": name, "description": desc}
    return render_template("departments/form.html", d=d, editing=True)


@bp.route("/<int:did>/delete", methods=["POST"])
@roles_required("admin")
def delete(did):
    db = get_db()
    if db.execute("SELECT 1 FROM doctors WHERE department_id=?", (did,)).fetchone():
        flash("Reassign or remove the doctors in this department first.", "danger")
    else:
        db.execute("DELETE FROM departments WHERE id=?", (did,))
        db.commit()
        flash("Department deleted.", "info")
    return redirect(url_for("departments.index"))
