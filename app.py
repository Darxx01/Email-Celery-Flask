import smtplib
from email.message import EmailMessage
from flask import Flask, request, render_template
from celery import Celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)

@app.route('/',methods=['GET','POST'])
def index():
  if request.method == 'POST':
    resultado = enviarEmail(request.form['asunto'], request.form['mensaje'], request.form['emailDestinatario'])
    # resultado.wait()
    return render_template('index.html', mensaje="Enviado!")

  return render_template('index.html')

@celery.task
def enviarEmail(asunto, msg, emailDestinatario):
  """
  Link de servidor: https://ethereal.email
  """
  
  mensaje = EmailMessage()

  sender_email_address = "hailie.daugherty@ethereal.email" 

  # Configure email headers 
  mensaje['Subject'] = asunto 
  mensaje['From'] = sender_email_address 
  mensaje['To'] = emailDestinatario
  mensaje.set_content(msg)

  email_smtp = "smtp.ethereal.email"  
  server = smtplib.SMTP(email_smtp, '587')

  server.ehlo() 
  server.starttls()
  server.login(sender_email_address, "fZZCXXG9WkbgjK2sEQ")
  server.send_message(mensaje) 
  server.quit()

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000, debug=True)
