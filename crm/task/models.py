from enum import Enum
from datetime import datetime

from crm.db import db, BaseModel


class TaskType(Enum):
    TASK, FEATURE, QUESTION, STORY, CONTACT = range(5)


class TaskPriority(Enum):
    MINOR, NORMAL, URGENT, CRITICAL = range(4)


class TaskState(Enum):
    NEW, PROGRESS, QUESTION, VERIFICATION, CLOSED = range(5)


class Task(db.Model, BaseModel):

    __tablename__ = "tasks"

    title = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    description = db.Column(
        db.Text(),
        default="",
        index=True
    )

    type = db.Column(
        db.Enum(TaskType),
        default=TaskType.TASK,
        index=True
    )

    priority = db.Column(
        db.Enum(TaskPriority),
        default=TaskPriority.MINOR,
        index=True
    )

    state = db.Column(
        db.Enum(TaskState),
        default=TaskState.NEW,
        index=True
    )

    assignee_id = db.Column(
        db.String,
        db.ForeignKey("users.id")
    )

    deadline = db.Column(
        db.TIMESTAMP,
        nullable=True,
        index=True
    )

    eta = db.Column(
        db.TIMESTAMP,
        nullable=True,
        index=True
    )

    # in hours
    time_estimate = db.Column(
        db.Integer,
        default=0
    )

    time_done = db.Column(
        db.Integer,
        default=0
    )

    company_id = db.Column(
        db.String,
        db.ForeignKey("companies.id")
    )

    contact_id = db.Column(
        db.String,
        db.ForeignKey("contacts.id")
    )

    user_id = db.Column(
        db.String,
        db.ForeignKey("users.id")
    )

    deal_id = db.Column(
        db.String,
        db.ForeignKey("deals.id")
    )

    organization_id = db.Column(
        db.String,
        db.ForeignKey("organizations.id")
    )

    project_id = db.Column(
        db.String,
        db.ForeignKey("projects.id")
    )

    sprint_id = db.Column(
        db.String,
        db.ForeignKey("sprints.id")
    )

    # alert_id = db.Column(
    #     db.String,
    #     db.ForeignKey("alerts.id")
    # )
    #
    # alert_source_id = db.Column(
    #     db.String,
    #     db.ForeignKey("alertsources.id")
    # )

    knowledge_base_id = db.Column(
        db.String,
        db.ForeignKey("knowledgebases.id")
    )

    comments = db.relationship(
        "Comment",
        backref="task"
    )

    messages = db.relationship(
        "Message",
        backref="task"
    )

    links = db.relationship(
        "Link",
        backref="task"
    )

    @property
    def percent_completed(self):
        done = 0.0
        for stat in self.tasks:
            done += stat.time_done
        if not done:
            return done
        if not self.time_todo:
            return 100
        return (done / self.time_todo) * 100

    def __str__(self):
        return self.title


class TaskTracking(db.Model, BaseModel):

    __tablename__ = "tasktrackings"

    # should be markdown.
    remarks = db.Column(
        db.Text()
    )

    time_done = db.Column(
        db.Integer,
        default=0
    )

    def __str__(self):
        return "<TaskTracker %s>" % self.id
