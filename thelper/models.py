import random
import pandas as pd
import numpy as np
from thelper import APP, DB
from thelper.admin_views import add_view

# TODO: Flask admin screens


# Bingo!
@add_view(cols=["description"], category="Other")
class Bingo(DB.Model):
    """Simple bingo-item"""

    id = DB.Column(DB.Integer, primary_key=True)
    description = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        return self.description


# Generic Tracker
@add_view(cols=["description"], category="Other")
class Activity(DB.Model):
    """Generic tracker"""

    id = DB.Column(DB.Integer, primary_key=True)
    description = DB.Column(DB.String, nullable=False)


# @add_view(cols=["datetime"], inline=["activity"])
class ActivityLog(DB.Model):
    """Generic tracker"""

    id = DB.Column(DB.Integer, primary_key=True)
    activity_id = DB.Column(DB.Integer, DB.ForeignKey("activity.id"))
    activity = DB.relationship("Activity")
    datetime = DB.Column(DB.DateTime)


# Teacher helper stuff
@add_view(
    cols=["first_name", "last_name", "full_name"],
    category="Classroom",
    # inline=[(Period,)],
)
class Student(DB.Model):
    """Basic student"""

    id = DB.Column(DB.Integer, primary_key=True)
    first_name = DB.Column(DB.String)
    last_name = DB.Column(DB.String)
    full_name = DB.Column(DB.String, unique=True)
    period_id = DB.Column(DB.Integer, DB.ForeignKey("period.id"))
    period = DB.relationship("Period", backref="students")

    def __repr__(self):
        return self.full_name


period_teacher = DB.Table(
    "period_teacher",
    DB.metadata,
    DB.Column("period_id", DB.Integer, DB.ForeignKey("period.id")),
    DB.Column("teacher_id", DB.Integer, DB.ForeignKey("teacher.id")),
)


@add_view(cols=["description", "group_counts"], category="Classroom")
class Period(DB.Model):
    """Group of students for randomizing pools"""

    id = DB.Column(DB.Integer, primary_key=True)
    description = DB.Column(DB.String, nullable=False)
    group_counts = DB.Column(DB.Integer, nullable=False, default=1)
    # teacher_id = DB.Column(DB.Integer, DB.ForeignKey("teacher.id"))
    teachers = DB.relationship("Teacher", secondary=period_teacher)

    def __repr__(self):
        return f"{self.description}: {len(self.teachers)} teachers, {len(self.students)} students"

    def generate_groups(self):
        """breakout a 'period' into random groups
        with associated random teacher(s)
        """
        # Shuffle teachers and extend to fill columns
        random.shuffle(self.teachers)
        cols = np.resize(self.teachers, self.group_counts)

        # Breat up a period's student list into constituent groups
        random.shuffle(self.students)
        delta = (
            self.group_counts - (len(self.students) % self.group_counts)
        ) % self.group_counts
        df = pd.DataFrame(
            np.reshape(
                # numpy doesn't like unmatched, so pad odd-values as None-s
                self.students + [None] * delta,
                (
                    # Rows extended to clean multiple
                    int((len(self.students) + delta) / self.group_counts),
                    # Columns
                    self.group_counts,
                ),
            ),
            columns=cols,
        )
        return df


@add_view(cols=["full_name"], category="Classroom")
class Teacher(DB.Model):
    """Basic student"""

    id = DB.Column(DB.Integer, primary_key=True)
    full_name = DB.Column(DB.String, unique=True)
    periods = DB.relationship("Period", secondary=period_teacher)

    def __repr__(self):
        return self.full_name