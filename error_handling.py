from flask import flash, redirect, url_for

def throw_span_ex(message):
    message = message or "Invalid operation" 
    flash(message, "Error")
    return redirect(url_for("routes.index"))