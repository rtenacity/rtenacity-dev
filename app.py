from flask import Flask, render_template, request
from forms import ContactForm
import pandas as pd
import boto3
from botocore.exceptions import ClientError

SENDER = "rtenacity@gmail.com"

RECIPIENT = "rtenacity@gmail.com"

AWS_REGION = "us-west-2"

SUBJECT = "New Alert"

BODY_TEXT = "This is from the website!"
            
CHARSET = "UTF-8"

client = boto3.client('ses',region_name=AWS_REGION)

app = Flask(__name__)
app.secret_key = 'dev fao football app'

@app.route("/", methods=["GET", "POST"])
def get_contact():
    form = ContactForm()
    if request.method == 'POST':   
        name = request.form["name"]
        email = request.form["email"] 
        message = request.form["message"]

        BODY_TEXT = "Name = " + name + "\n" + "Email = " + email + "\n" + "Message = " + message

        try:
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
        return render_template('index.html', form=form)

    else:
        return render_template('index.html', form=form)
    return print("hello")
    if form.validate_on_submit():
            # do stuff with valid form
            # then redirect to "end" the form
        return redirect(url_for('register'))

if __name__ == "__main__":
    app.run(host="localhost", port=80, debug=True) 

#FLASK_APP=app.py FLASK_DEBUG=1 sudo flask run -h 0.0.0.0 -p 80

