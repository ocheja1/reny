from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from .models import Property
from .forms import PropertyForm
from . import db

views = Blueprint('views', __name__)


@views.route('/')
def index():
    return render_template('index.html')


@views.route('/property/create', methods=['GET', 'POST'])
@login_required
def create_property():
    form = PropertyForm()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            # Extract form data
            first_name = form.first_name.data
            last_name = form.last_name.data
            landlord_address = form.landlord_name.data
            property_type = form.property_type.data
            number_of_beds = form.number_of_beds.data
            location = form.location.data
            state = form.state.data
            lga = form.lga.data
            street = form.street.data
            price = float(form.price.data)  # Convert the price to float
            youtube_links = form.youtube_links.data

            image_file = form.image_upload.data  # Access the uploaded file

            if image_file:
                # Read binary image data
                image_data = image_file.read()

                # Create a new Property object using the form data, including the image data
                new_property = Property(
                    landlord_id=current_user.id,
                    first_name=first_name,
                    last_name=last_name,
                    landlord_address=landlord_address,
                    property_type=property_type,
                    number_of_beds=number_of_beds,
                    location=location,
                    state=state,
                    lga=lga,
                    street=street,
                    price=price,
                    image_data=image_data,  # Store binary image data
                    youtube_links=youtube_links
                )

                # Add the Property object to the database session and commit
                db.session.add(new_property)
                db.session.commit()

                flash('Property added!', category='success')
                return redirect(url_for('views.index'))

        except Exception as e:
            # Handle any unexpected errors gracefully
            flash(f'An error occurred: {str(e)}', category='danger')

    # If there are validation errors or if the request method is GET, show the form
    return render_template('PropertyForm.html', form=form)
