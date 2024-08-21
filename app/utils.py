from functools import wraps
from flask import flash, redirect, request, url_for
from flask_login import current_user
from . import app

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def get_list_url(peran=None):
    links = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            if peran:
                if peran in rule.endpoint:
                    url = url_for(rule.endpoint)
                    links.append((url, rule.endpoint))
            else:
                url = url_for(rule.endpoint)
                links.append((url, rule.endpoint))
    return links

def peran_required(peran):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            route = request.endpoint

            if not current_user.is_authenticated:
                flash('Anda harus login terlebih dahulu.', 'error')
                return redirect(url_for('auth.login'))

            list_url = get_list_url(current_user.peran)

            if any(route in t for t in list_url):
                print(route)
                flash('Anda tidak memiliki akses ke halaman ini.', 'error')
                return redirect(url_for(current_user.peran + '.dashboard'))

            # for url, endpoint in list_url:
            #     if route == url:
            #         return redirect(url_for(endpoint))

            return func(*args, **kwargs)
        return wrapper
    return decorator
