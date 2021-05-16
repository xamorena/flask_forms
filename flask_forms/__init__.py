import json

import flask
import flask_wtf
import wtforms.fields.html5
import wtforms.widgets


class CheckField(wtforms.fields.Field):

    widget = wtforms.widgets.CheckboxInput()
    false_values = (0, "0", "")

    def __init__(self, label=None, validators=None, false_values=None, **kwargs):
        super().__init__(label, validators, **kwargs)
        if false_values is not None:
            self.false_values = false_values

    def process_data(self, value):
        self.data = int(value) if value in ["0", "1", 0, 1] else 0

    def process_formdata(self, valuelist):
        if not valuelist or valuelist[0] in self.false_values:
            self.data = 0
        else:
            self.data = 1

    def _value(self):
        if self.raw_data:
            return str(self.raw_data[0])
        return "1"



class TestForm(flask_wtf.FlaskForm):
    test_text = wtforms.fields.StringField(label="Test")
    test_textarea = wtforms.fields.TextAreaField(label="Textarea")
    test_code = wtforms.fields.html5.DecimalField(label="Code")
    test_date = wtforms.fields.html5.DateField(label="Date")
    test_time = wtforms.fields.html5.TimeField(label="Time")
    test_datetime = wtforms.fields.html5.DateTimeField(label="Date-time")
    test_email = wtforms.fields.html5.EmailField(label="Email")
    test_check = CheckField(label="Check")
    test_search = wtforms.fields.html5.SearchField(label="Search")


app = flask.Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = b'ABCDEF123456789'


@app.route("/", methods=["GET"])
def get_test_form():
    form = TestForm()
    if flask.request.args.get("test_check") in ["0", "1"]:
        form.test_check.data = int(flask.request.values["test_check"])
    return flask.render_template("form.html", form=form, data=None)


@app.route("/", methods=["POST"])
def post_test_form():
    form = TestForm()
    return flask.render_template("form.html", form=form, data=json.dumps(form.data, indent=4))
