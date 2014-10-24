import web
from web import form
import RPi.GPIO as GPIO

#dont bug me with warnings
GPIO.setwarnings(False)

# to use Raspberry Pi bcm numbers
GPIO.setmode(GPIO.BCM)

# set up GPIO output channels
GPIO.setup(28, GPIO.OUT)  # Green
GPIO.setup(29, GPIO.OUT)  # Red
GPIO.setup(30, GPIO.OUT)  # Blue

# Green LED at pin 28, 500 Hz
G = GPIO.PWM(28, 500)
# Start off
G.start(100)
R = GPIO.PWM(29, 500)
R.start(100)
B = GPIO.PWM(30, 500)
B.start(100)

render = web.template.render('templates/')

urls = ('/', 'index')
app = web.application(urls, globals())

myform = form.Form(
    form.Textbox("Red",
        form.notnull,
        form.regexp('\d+', 'Must be a digit'),
        form.Validator('Must be more than 0', lambda x: int(x) >= 0),
        form.Validator('Must be less than 100', lambda x: int(x) <= 255)),
    form.Textbox("Green",
        form.notnull,
        form.regexp('\d+', 'Must be a digit'),
        form.Validator('Must be more than 0', lambda x: int(x) >= 0),
        form.Validator('Must be less than 100', lambda x: int(x) <= 255)),
    form.Textbox("Blue",
        form.notnull,
        form.regexp('\d+', 'Must be a digit'),
        form.Validator('Must be more than 0', lambda x: int(x) >= 0),
        form.Validator('Must be less than 100', lambda x: int(x) <= 255)),
    )


class index:
    def GET(self):
        form = myform()
        # make sure you create a copy of the form by calling it (line above)
        # Otherwise changes will appear globally
        return render.ledpi(form)

    def POST(self):
        form = myform()
        if not form.validates():
            return render.ledpi(form)
        else:
            #print form.d.Red
            #print form.d.Green
            #print form.d.Blue

            # Convert intputs to int
            IntRed = int(form.d.Red)
            IntGreen = int(form.d.Green)
            IntBlue = int(form.d.Blue)

            # Subtract input from 255 to get positive numbers
            R256 = 255 - IntRed
            G256 = 255 - IntGreen
            B256 = 255 - IntBlue
            #print R256
            #print G256
            #print B256

            print '#%02x%02x%02x' % (IntRed, IntGreen, IntBlue)

            # Divide number by 2.55 to get value out of 100
            # And set the duty cycle of the LED
            R.ChangeDutyCycle(R256 / 2.55)
            G.ChangeDutyCycle(G256 / 2.55)
            B.ChangeDutyCycle(B256 / 2.55)

            return render.ledpi(form)

if __name__ == "__main__":
    web.internalerror = web.debugerror
    app.run()

#R.stop()
#G.stop()
#B.stop()
#GPIO.cleanup()