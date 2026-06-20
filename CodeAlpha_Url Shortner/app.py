from flask import Flask,redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy
import random
import string

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)


class Url(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    short_url=db.Column(db.String(10),unique=True,nullable=False)
    Orignal_url=db.Column(db.String(500),nullable=False)
    
    
def generate_short_code():
    letters = string.ascii_letters  
    while True:
        code = ''.join(random.choices(letters, k=3))
        existing = Url.query.filter_by(short_url=code).first()
        if not existing:
            return code   
    
@app.route('/',methods=['POST','GET'])
def index():
   
    if request.method=='POST':
        url_input=request.form.get('url_input')
        # checking if already present
        found_url=Url.query.filter_by(Orignal_url=url_input).first()
        if found_url:
            return render_template(
            'index.html',
            message=f"This URL already exists. Short URL: {found_url.short_url}"
        )

        else:
            # create short url
            short_code=generate_short_code()
            new_url = Url(
            short_url=short_code,
            Orignal_url=url_input)
            db.session.add(new_url)
            db.session.commit()

            return render_template(
                'url_page.html',
                message="URL created successfully",
                url_display=short_code,
                original_url=url_input
    )
    else:
        return render_template('index.html')    
    #   to display success only
@app.route('/display/<short_url>')
def display_url(short_url):
    return render_template(
        'url_page.html',
        url_display=short_url
    )
    #  redirection to main page using short url
@app.route('/<short_url>')
def redirection(short_url):
    long_url=Url.query.filter_by(short_url=short_url).first()
    if long_url:
        return redirect(long_url.Orignal_url)

    return "<h1>URL does not exist in our DB</h1>"
    
@app.route('/all_urls')
def all_urls():
    urls = Url.query.all()

    return render_template(
        'all_urls.html',
        urls=urls
    )
    
    
if __name__== '__main__':
   
   with app.app_context():
       db.create_all()
    
   app.run(debug=True)    
   






