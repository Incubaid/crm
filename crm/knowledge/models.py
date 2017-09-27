# from crm.db import db, BaseModel
#
#
# class KnowledgeBase(db.Model, BaseModel):
#
#     __tablename__ = "knowledgebases"
#
#     title = db.Column(
#         db.String(255),
#         nullable=False
#     )
#
#     category_id = db.Column(
#         db.String(5),
#         db.ForeignKey("categories.id")
#     )
#
#     author_id = db.Column(
#         db.String(5),
#         db.ForeignKey("users.id")
#     )
#
#     content = db.Column(
#         db.Text()
#     )
#
#     tasks = db.relationship(
#         "Task",
#         backref="knowledgebase"
#     )
#
#     comments = db.relationship(
#         "Comment",
#         backref="knowledgebase"
#     )
#
#
# class KnowledgeBaseCategory(db.Model, BaseModel):
#
#     __tablename__ = "categories"
#
#     name = db.Column(
#         db.String(255),
#         nullable=False
#     )
#
#     description = db.Column(
#         db.Text()
#     )
#
#     knowledges = db.relationship(
#         "KnowledgeBase",
#         backref="category"
#     )
