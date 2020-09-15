"""decorator to create flask-admin classes"""
from flask_admin.contrib.sqla import ModelView
from thelper import DB

# flask-admin crud
admin_views = {}
# Simple json response
api_endpoints = {}


class MyModelView(ModelView):
    column_display_pk = True
    can_set_page_size = True
    can_export = True
    export_types = ["csv", "json", "xlsx"]
    column_hide_backrefs = False


def add_view(cols: list = None, category: str = "Finance", inline: list = None):
    """generate a basic admin view for this class"""

    def decorate(func):
        """Generate new View class and add to dict"""
        # Common attributes
        atts = {
            att: cols
            for att in [
                "column_editable_list",
                "column_searchable_list",
                "column_filters",
            ]
        }
        atts["category"] = category
        atts["model"] = func
        atts["session"] = DB.session
        atts["inline_models"] = inline
        # Name for generated view class
        name = f"{func.__name__}GenView"
        new = type(name, (MyModelView,), atts)
        admin_views[name] = {
            "type": new,
            "model": func,
            "session": DB.session,
            "category": category,
        }
        api_endpoints[func.__name__.lower()] = func
        return func

    return decorate
