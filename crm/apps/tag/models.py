from crm.db import db, BaseModel


class Tag(db.Model, BaseModel):
    """
    Model for any kind of tags
    """

    __tablename__ = "tags"

    tag = db.Column(
        db.String(),
        nullable=False,
        unique=True,
        index=True
    )

    companies = db.relationship(
        "Company",
        secondary="companies_tags",
        backref="tags"
    )

    def __str__(self):
        return self.tag