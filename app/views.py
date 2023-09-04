from flask import Blueprint, render_template, send_file, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Property
from . import db

views = Blueprint('views', __name__)


@views.route('/')
def index():
    return render_template('index.html')


@views.route('/property/create', methods=['GET', 'POST'])
@login_required
def create_property():
    if request.method == 'POST':
        # Extract form data
        title = request.form.get('property-title')
        property_type = request.form.get('property-type')
        number_of_beds = request.form.get('numberofbeds')
        location = request.form.get('location')
        state = request.form.get('state')
        lga = request.form.get('lga')
        street = request.form.get('street')
        price = request.form.get('price')
        youtube_links = request.form.get('youtube-links')

        # Create a new Property object using the data
        new_property = Property(
            title=title,
            property_type=property_type,
            number_of_beds=number_of_beds,
            location=location,
            state=state,
            lga=lga,
            street=street,
            price=price,
            youtube_links=youtube_links,
            landlord=current_user  # Associate the property with the current user (landlord)
        )

        # Add the property to the database and commit the changes
        db.session.add(new_property)
        db.session.commit()

        flash('Property added!', category='success')
        return redirect(url_for('views.index'))

    return render_template(url_for('create_property'))
