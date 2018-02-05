from datetime import datetime
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
                    task.assignee.admin_view_link(), str(task.assignee))
            else:
                task_formatted += " not assigned "
            task_formatted += "  (Updated at: {} )".format(
                task.updated_at.strftime("%Y-%m-%d"))
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
        return value.strftime("%Y-%m-%d")


def format_messages(view, context, model, name):
    value = getattr(model, name)
    out = "<ul>"

    auto_tasks = []
    if isinstance(value, InstrumentedList):
        for x in value:
            if x.title.startswith('You have a new assigned task') or x.title.startswith('Your assigned task has been updated'):
                auto_tasks.append(x)
                continue
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

def format_referrer1_deals(view, context, model, name):
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
    for x in value:
        out += '<li><a href="mailto:{email}">{email}</a></li>'.format(email=x.email)
    out += "</ul>"
    return Markup(out)


def format_telephones(view, context, model, name):
    value = getattr(model, name)
    if not value:
        return ''
    out = "<ul>"
    for x in value:
        out += '<li><a href="tel:{telephone}">{telephone}</a></li>'.format(telephone=x.telephone)
    out += "</ul>"
    return Markup(out)


def format_notification_emails(view, context, model, name):
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


def format_user_no_markup(view, context, model, name):
    value = getattr(model, name)
    if not value:
        return ''

    return '{firstname} {lastname}'.format(firstname=value.firstname, lastname=value.lastname).strip() or value


def format_time_sent(view, context, model, name):
    value = getattr(model, name)
    if not value:
        return ''
    return value.strftime('%H:%M:%S %p %Z').strip()


format_start = format_datetime
format_end=  format_datetime


def format_last_login(view, context, model, name):
    value = getattr(model, name)
    if not value:
        return ''
    return value.strftime('%Y-%b-%d %H:%M:%S %p %Z').strip()

def format_user(view, context, model, name):
    value = getattr(model, name)
    if not value:
        return ''
    return Markup('<a href="/user/details/?id={id}">{username}</a>'.format(id=value.id, username=value.username))

column_formatters = dict(
    list(zip(["users", "contacts", "companies", "organizations", "projects",  "deals", "sprints", 'events',
                                   "links", "messages", "ownsTasks", "ownsContacts", "ownsCompanies",
                                   "ownsOrganizations", "ownsSprints", "ownsAsBackupContacts", "ownsAsBackupCompanies"], cycle([format_instrumented_list]))),
    telephones=format_telephones, website=format_url, destination=format_notification_emails,
    tasks=format_tasks,
    messages=format_messages, comments=format_comments, url=format_url, emails=format_emails,
    images=format_images, image=format_image,
    author_last=format_author,
    author_original=format_author,
    replies=format_messages,
    time_sent=format_time_sent,
    last_login=format_last_login,
    start=format_start,
    end=format_end,
    referrer1_deals=format_referrer1_deals,
    ownsDeals=format_referrer1_deals,
)

column_formatters = {**column_formatters, **
                     dict(list(zip(["created_at", "updated_at", "closed_at", "start_date", "deadline", "eta"], cycle([format_datetime]))))}

column_formatters = {**column_formatters, **
                     dict(list(zip(["description", "bio", "belief_statement", "content"], cycle([format_markdown]))))}
