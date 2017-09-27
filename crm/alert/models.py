# from enum import Enum
#
# from crm.db import db, BaseModel
#
#
# class AlertProfile(db.Model, BaseModel):
#
#     __tablename__ = "alertprofiles"
#
#     name = db.Column(
#         db.String(255),
#         nullable=False
#     )
#
#     decription = db.Column(
#         db.Text()
#     )
#
#     # toml config.
#     configuration = db.Column(
#         db.Text()
#     )
#
#     alert_id = db.Column(
#         db.String,
#         db.ForeignKey("alerts.id")
#     )
#
#
# class AlertSource(db.Model, BaseModel):
#
#     __tablename__ = "alertsources"
#
#     title = db.Column(
#         db.String(255),
#         nullable=False
#     )
#
#     description = db.Column(
#         db.Text()
#     )
#
#     comments = db.relationship(
#         "Comment",
#         backref="alertsource"
#     )
#
#     links = db.relationship(
#         "Link",
#         backref="alertsources"
#     )
#
#     projects = db.relationship(
#         "Project",
#         backref="alertsources",
#         uselist=False
#     )
#
#     tasks = db.relationship(
#         "Task",
#         backref="alertsources",
#         uselist=False
#     )
#
#     alerts = db.relationship(
#         "Alert",
#         backref="source"
#     )
#
#     @property
#     def source_id(self):
#         pass
#
#
# class AlertState(Enum):
#     NEW, CONFIRMED, CLOSED = range(3)
#
#
# class AlertUrgency(Enum):
#     CRITICAL, URGENT, NORMAL, MINOR = range(4)
#
#
# class EscalationLevel(Enum):
#     YELLOW, ORANGE, RED, GREEN = range(4)
#
#
# class Alert(db.Model, BaseModel):
#
#     __tablename__ = "alerts"
#
#     title = db.Column(
#         db.String(255),
#         nullable=False
#     )
#
#     # source_id = source.source_id
#     alert_source_id = db.Column(
#         db.String(5),
#         db.ForeignKey("alertsources.id")
#     )
#
#     content = db.Column(
#         db.Text()
#     )
#
#     category = db.Column(
#         db.String(255)
#     )
#
#     device_uid = db.Column(
#         db.String(255)
#     )
#
#     component_uid = db.Column(
#         db.String(255)
#     )
#
#     state = db.Column(
#         db.Enum(AlertState),
#         default=AlertState.NEW
#     )
#
#     urgency = db.Column(
#         db.Enum(AlertUrgency),
#         default=AlertUrgency.CRITICAL
#     )
#
#     escalation_level = db.Column(
#         db.Enum(EscalationLevel),
#         default=EscalationLevel.YELLOW
#     )
#
#     # relations
#     profile = db.relationship(
#         "AlertProfile",
#         backref="alert"
#     )
#
#     task = db.relationship(
#         "Task",
#         backref="alert"
#     )
#
#     comments = db.relationship(
#         "Comment",
#         backref="alert"
#     )
#
#     links = db.relationship(
#         "Link",
#         backref="alert"
#     )
#
#     owner_id = db.Column(
#         db.String(5),
#         db.ForeignKey('users.id')
#     )
#
#     @property
#     def start_time(self):
#         pass
#
#     @property
#     def close_time(self):
#         pass
