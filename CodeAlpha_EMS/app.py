from flask import Flask, redirect,url_for,render_template,flash
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm,RegisterForm,EventForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db,User,Event,Booking
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///EMS.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "ali123"

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "Login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def Home():
    return render_template('home.html')
    

@app.route('/register',methods=['POST','GET'])
def Register():
 form=RegisterForm()
 if form.validate_on_submit():
   

    if form.password.data == form.confirm_password.data:
       hash_password=generate_password_hash(form.password.data)
       New_user=User(
                username=form.username.data,
                email=form.email.data,
                password=hash_password
       )
       db.session.add(New_user)
       db.session.commit()
       flash("Registration successful. Please login.", "success")
       return redirect('/login')

 return render_template('register.html',form=form)
    

@app.route('/login', methods=['POST', 'GET'])
def Login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful.", "success")
            return redirect('/dashboard')

        flash("Invalid email or password.", "danger")

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def Logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for('Login'))


@app.route('/dashboard')
@login_required
def UserDashboard():

    return render_template('dashboard.html')



@app.route('/create_event',methods=['POST','GET'])
@login_required
def Create_Event():
    
    if current_user.role !='admin':
       return 'Access Denied'
    
    form=EventForm()
    if form.validate_on_submit():
       event=Event(
        title=form.title.data,
        description=form.description.data,
        date=form.date.data,
        location=form.location.data,
        capacity=form.capacity.data,
        phone=form.phone.data
       )
       db.session.add(event)
       db.session.commit()
       flash("Event created successfully.", "success")
       return redirect ('/events')

    return render_template('create_event.html',form=form)

@app.route('/events')
@login_required
def ViewEvents():
   events=Event.query.all()

   return render_template('view_events.html',events=events)


@app.route('/edit-event/<int:id>',methods=['GET','POST'])
@login_required
def EditEvent(id):
    if current_user.role != 'admin':
        return "Access Denied"

    event = Event.query.get_or_404(id)

    form = EventForm(obj=event)

    if form.validate_on_submit():

        event.title = form.title.data
        event.description = form.description.data
        event.location = form.location.data
        event.date = form.date.data
        event.capacity = form.capacity.data
        event.phone = form.phone.data

        db.session.commit()
        flash("Event updated successfully.", "success")
        return redirect('/events')

    return render_template(
        'edit_event.html',
        form=form
    )


@app.route('/delete-event/<int:id>')
@login_required
def DeleteEvent(id):

    if current_user.role != 'admin':
        return "Access Denied"

    event = Event.query.get_or_404(id)

    db.session.delete(event)
    db.session.commit()
    flash("Event deleted successfully.", "danger")
    return redirect('/events')

@app.route('/book/<int:event_id>')
@login_required
def BookEvent(event_id):

    event = Event.query.get_or_404(event_id)

    existing_booking = Booking.query.filter_by(
        user_id=current_user.id,
        event_id=event.id
    ).first()

    if existing_booking:
        flash("You already booked this event.", "warning")
        return redirect('/events')

    total_bookings = Booking.query.filter_by(
        event_id=event.id
    ).count()

    if total_bookings >= event.capacity:
        flash("Event is full.", "danger")
        return redirect('/events')

    booking = Booking(
        user_id=current_user.id,
        event_id=event.id
    )

    db.session.add(booking)
    db.session.commit()

    flash("Event booked successfully.", "success")
    return redirect('/my-bookings')

@app.route('/my-bookings')
@login_required
def MyBookings():

    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        'my_booking.html',
        bookings=bookings
    )

@app.route('/cancel-booking/<int:id>')
@login_required
def CancelBooking(id):

    booking = Booking.query.get_or_404(id)

    if booking.user_id != current_user.id:
        return "Access Denied"

    db.session.delete(booking)
    db.session.commit()
    flash("Booking cancelled.", "info")
    return redirect('/my-bookings')



@app.route('/all-bookings')
@login_required
def AllBookings():

    if current_user.role != 'admin':
        return "Access Denied"

    bookings = Booking.query.all()

    return render_template(
        'all_bookings.html',
        bookings=bookings
    )



if __name__ ==("__main__"):   
    with app.app_context():
        db.create_all()
    app.run(debug=True)

