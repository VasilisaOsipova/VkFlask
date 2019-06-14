from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.validators import DataRequired


class AnalyzeForm(FlaskForm):
    domains = TextField("domains", validators=[DataRequired()],
                        render_kw={"placeholder": "Сообщества"})
    tags = TextField("tags", validators=[DataRequired()],
                     render_kw={"placeholder": "Ключевые слова"})
