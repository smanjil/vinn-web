
import arrow
from config import app

@app.template_filter()
def date_humanize(date):
    return arrow.get(date).replace(tzinfo='local').humanize()
