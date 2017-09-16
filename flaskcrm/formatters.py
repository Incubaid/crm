from itertools import cycle
from sqlalchemy.orm.collections import InstrumentedList
from jinja2 import Markup
from flask_misaka import markdown


def format_instrumented_list(view, context, model, name):

    value = getattr(model, name)
    out = ""
    if isinstance(value, InstrumentedList):
        out = "<ul>"
        for x in value:
            if x is None:  # items can be created from empty forms in the form. let's fix that in the model
                continue
            if hasattr(x, "admin_view_link"):
                out += "<li><a href='{}'>{}</a></li>".format(
                    getattr(x, "admin_view_link")(), x)
            else:
                out += str(x)
        out += "</ul>"
    return Markup(out)


def format_url(view, context, model, name):
    value = getattr(model, name)
    return Markup("<a href='{url}'>{url}</a>".format(url=value))


def format_datetime(view, context, model, name):
    value = getattr(model, name)
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")


def format_comments(view, context, model, name):
    value = getattr(model, name)
    out = ""

    if isinstance(value, InstrumentedList):
        out = "<ul>"
        for x in value:
            if hasattr(x, "admin_view_link"):
                out += "<li>{commentcontent}<a href='{commentadminlink}'> Read more...</a></li>".format(
                    commentadminlink=getattr(x, "admin_view_link")(), commentcontent=x.content)
            else:
                out += str(x)
        out += "</ul>"
    return Markup(out)


def format_description(view, context, model, name):
    value = getattr(model, name)
    if value:
        return markdown(value)
    return value


def format_emails(view, context, model, name):
    value = getattr(model, name)
    out = "<ul>" 
    for x in value:
        out += '<li><a href="mailto:{email}">{email}</a></li>'.format(email=x)
    out += "</ul>"
    return Markup(out)


column_formatters = dict(list(zip(["telephones", "users", "contacts", "organizations", "projects",  "deals", "sprints",
                            "links", "tasks", "messages"], cycle([format_instrumented_list]))), comments=format_comments, url=format_url, emails=format_emails, description=format_description)

column_formatters = {**column_formatters, **
              dict(list(zip(["created_at", "updated_at", "closed_at", "start_date", "deadline", "eta"], cycle([format_datetime]))))}

