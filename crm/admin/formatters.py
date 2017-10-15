from datetime import datetime
from itertools import cycle
from sqlalchemy.orm.collections import InstrumentedList
from jinja2 import Markup
from flask_misaka import markdown
from crm.settings import IMAGES_DIR


def format_instrumented_list(view, context, model, name):

    value = getattr(model, name)
    out = ""
    if isinstance(value, InstrumentedList):
        out = "<ul>"
        for x in value:
            if x is None:
                continue
            if hasattr(x, "admin_view_link"):
                out += "<li><a href='{}'>{}</a></li>".format(
                    getattr(x, "admin_view_link")(), x)
            else:
                out += str(x)
        out += "</ul>"
    return Markup(out)


def format_tasks(view, context, model, name):
    value = getattr(model, name)
    out = ""
    if isinstance(value, InstrumentedList):
        out = "<ul>"
        for task in value:
            task_formatted = "<a href={}>{}</a>".format(
                task.admin_view_link(), task)
            if task.assignee is not None:
                task_formatted += " assigned to <a href='{}'>{}</a> ".format(
                    task.assignee.admin_view_link(), task.assignee.username)
            else:
                task_formatted += " not assigned "
            task_formatted += "  (Updated at: {} )".format(
                task.updated_at.strftime("%Y-%m-%d %H:%M"))
            out += "<li>{}</li>".format(task_formatted)

        out += "</ul>"
    return Markup(out)


def format_url(view, context, model, name):
    value = getattr(model, name)
    if value:
        return Markup("<a href='{url}'>{url}</a>".format(url=value))


def format_datetime(view, context, model, name):
    value = getattr(model, name)
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M")


def format_messages(view, context, model, name):
    value = getattr(model, name)
    out = "<ul>"

    if isinstance(value, InstrumentedList):
        for x in value:
            if hasattr(x, "admin_view_link"):
                out += "<li>({authorname}/{messagetitle}/{createdate}) wrote: <br/> {messagecontent}<a href='{messageadminlink}'> Read more...</a></li>".format(
                    authorname=str(x.user),
                    messagetitle=x.title,
                    createdate=str(x.created_at_short),
                    messageadminlink=getattr(x, "admin_view_link")(),
                    messagecontent=x.content)
            else:
                out += str(x)
    out += "</ul>"
    return Markup(out)


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


def format_markdown(view, context, model, name):
    value = getattr(model, name)
    if value:
        return markdown(value)
    return value


def format_emails(view, context, model, name):
    value = getattr(model, name)
    if not value:
        return ''
    out = "<ul>"
    for x in value.split(','):
        out += '<li><a href="mailto:{email}">{email}</a></li>'.format(email=x)
    out += "</ul>"
    return Markup(out)


def format_telephones(view, context, model, name):
    value = getattr(model, name)
    if not value:
        return ''
    out = "<ul>"
    for x in value.split(','):
        out += '<li>{telephone}</li>'.format(telephone=x)
    out += "</ul>"
    return Markup(out)


def format_destination_emails(view, context, model, name):
    value = getattr(model, name)
    formatted_values = [
        '<a href="mailto:{email}">{email}</a>'.format(email=item) for item in value]
    return Markup(", ".join(formatted_values))


def format_images(view, context, model, name):
    value = getattr(model, name)
    if not value:
        return ''
    out = "<ul>"
    for x in value:
        if x.path:
            out += '<li>{}</li>'.format(
                x.as_image)
    out += "</ul>"
    return Markup(out)


def format_image(view, context, model, name):
    value = getattr(model, name)
    if not value:
        return ''

    return Markup(value.as_image)


def format_author(view, context, model, name):
    value = getattr(model, name)
    if not value:
        return ''

    return value


column_formatters = dict(
    list(zip(["users", "contacts", "companies", "organizations", "projects",  "deals", "sprints",
                                   "links", "messages", "ownsTasks", "ownsContacts", "ownsCompanies",
                                   "ownsOrganizations", "ownsSprints", "ownsAsBackupContacts", "ownsAsBackupCompanies"], cycle([format_instrumented_list]))),
    telephones=format_telephones, website=format_url, destination=format_destination_emails,
    tasks=format_tasks,
    messages=format_messages, comments=format_comments, url=format_url, emails=format_emails,
    images=format_images, image=format_image,
    author_last=format_author,
    author_original=format_author,
)

column_formatters = {**column_formatters, **
                     dict(list(zip(["created_at", "updated_at", "closed_at", "start_date", "deadline", "eta"], cycle([format_datetime]))))}

column_formatters = {**column_formatters, **
                     dict(list(zip(["description", "bio", "belief_statement", "content"], cycle([format_markdown]))))}
