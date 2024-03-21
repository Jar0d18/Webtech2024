from website import app, db
from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from website.models import Bungalowpark, User, Reservering
from website.forms import LoginForm, RegistrationForm, ReservationForm



def load_user(user_id):
    return User.query.get(int(user_id))



class Bungalow(db.Model):
    __tablename__ = 'bungalow'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    type = db.Column(db.String(80), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    week_price = db.Column(db.Float, nullable=False)
    park_id = db.Column(db.Integer, db.ForeignKey('bungalowpark.id'), nullable=False)
    
class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)
    bungalow_id = db.Column(db.Integer, db.ForeignKey('bungalow.id'), nullable=False)
    week = db.Column(db.Integer, nullable=False)

with app.app_context():
    def validate_reservering(form):
        bungalow = form.get('bungalow')
        type = form.get('type')
        grootte = form.get('grootte')
        week = form.get('week')

        if not bungalow:
            return 'Bungalow is vereist'
        if not type:
            return 'Type is vereist'
        if not grootte:
            return 'Grootte is vereist'
        try:
            grootte = int(grootte)
        except ValueError:
            return 'Grootte moet een getal zijn'
        if not week:
            return 'Week is vereist'
        try:
            week = int(week)
        except ValueError:
            return 'Week moet een getal zijn'
        if week < 1 or week > 52:
            return 'Week moet tussen 1 en 52 liggen'

        return None

    @app.route('/reservering', methods=['get','POST'])
    @login_required
    def reservering():
        form = ReservationForm()
        if form.validate_on_submit():
            # Check if bungalow exists
            bungalow = Bungalowpark.query.filter_by(id=form.bungalow.data).first()
            if bungalow is None:
                error = 'Bungalow does not exist'
                return render_template('reservering.html', form=form, error=error)

            # Check if week is available
            week = form.week.data
            existing_reservations = Reservering.query.filter_by(bungalow=bungalow, week=week).all()
            if len(existing_reservations) > 0:
                error = 'Week is not available'
                return render_template('reservering.html', form=form, error=error)

             # Create new reservation
            bungalow_naam = form.bungalow.data
            type = form.type.data
            grootte = form.grootte.data
            week = form.week.data
            reservering = Reservering(bungalow=bungalow_naam, type=type, grootte=grootte, week=week, user_id=current_user.id)
            db.session.add(reservering)
            db.session.commit()

            flash('Reservation made successfully')
            return redirect(url_for('reservering'))

        # Get user's reservations
        reserveringen = Reservering.query.filter_by(user_id=current_user.id).all()

        return render_template('reservering.html', form=form, reserveringen=reserveringen)



    @app.route('/registratie', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit() and form.check_email(form.email) and form.check_username(form.username):
            user = User(email=form.email.data, username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Dank voor de registratie. Er kan nu ingelogd worden!')
            return redirect(url_for('login'))
        return render_template('registratie.html', form=form)




    @app.route('/bevestig_registratie')
    def bevestig_registratie():
        gebruikers = User.query.all()
        return render_template('inlog.html', gebruikers=gebruikers)




    @app.route('/bungalows')
    def bungalows():
        return render_template('bungalows.html')
    
    @app.route('/faciliteiten')
    def faciliteiten():
        return render_template('faciliteiten.html')
    
    @app.route('/Activiteiten')
    def activiteiten():
        return render_template('activiteiten.html')

    

    

    @app.before_first_request
    def create_all():
        db.create_all()

    @app.route('/inlog', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None and user.check_password(form.password.data): 
                login_user(user)
                session['role'] = 'user' # get from DB: user.role
                flash('Succesvol ingelogd.')
                next = request.args.get('next')
                if next == None or not next[0]=='/':
                    next = url_for('inloghomepagina')
                return redirect(next)
            else:
                flash('Inlog mislukt.')
        return render_template('inlog.html', form=form)
    



    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Je bent nu uitgelogd!')
        return render_template('/index.html')


    @app.route('/inloghomepagina')
    @login_required
    def inloghomepagina():
        return render_template('inloghomepagina.html')

    
    @app.route('/')
    def index():
        return render_template('index.html')

    
    if __name__ == '__main__':
        app.run(debug=True)

