from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

membership_bp = Blueprint("membership", __name__)

@membership_bp.route("/membership-benifits")
def MembershipBenifits():
    return render_template("screens/membership/m_benifits.html")

@membership_bp.route("/online-application", methods=['GET', 'POST'])
def OnlineApplication():
    if request.method == 'POST':
        try:
            # Get form data
            form_data = {
                'full_name': request.form.get('fullName'),
                'email': request.form.get('email'),
                'phone': request.form.get('phone'),
                'date_of_birth': request.form.get('dob'),
                'organization': request.form.get('organization'),
                'designation': request.form.get('designation'),
                'research_interests': request.form.get('researchInterests'),
                'address': request.form.get('address'),
                'city': request.form.get('city'),
                'state': request.form.get('state'),
                'country': request.form.get('country'),
                'pincode': request.form.get('pincode'),
                'membership_type': request.form.get('membershipType'),
                'application_date': datetime.utcnow().isoformat(),
                'status': 'pending'
            }

            print("Form data collected:", form_data)  # Debug print

            # Handle CV file upload
            if 'cv' in request.files:
                cv_file = request.files['cv']
                if cv_file and cv_file.filename:
                    try:
                        # Secure the filename
                        filename = secure_filename(cv_file.filename)
                        unique_filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{filename}"
                        file_path = f"cv_documents/{unique_filename}"
                        file_data = cv_file.read()
                        
                        print("Attempting file upload to storage...")  # Debug print
                        
                        # Upload to Supabase Storage
                        storage_response = supabase.storage.from_('membership_documents').upload(
                            file_path,
                            file_data,
                            {'content-type': 'application/pdf'}
                        )
                        
                        print("File uploaded successfully:", storage_response)  # Debug print
                        form_data['cv_file_path'] = file_path
                        
                    except Exception as file_error:
                        print(f"File upload error: {str(file_error)}")  # Debug print
                        raise Exception(f"Error uploading file: {str(file_error)}")

            print("Attempting to insert data into database...")  # Debug print
            
            # Insert data into Supabase
            result = supabase.table('membership_applications').insert(form_data).execute()
            
            print("Data inserted successfully:", result)  # Debug print

            flash('Application submitted successfully! We will review your application and contact you soon.', 'success')
            return redirect(url_for('membership.OnlineApplication'))

        except Exception as e:
            error_message = str(e)
            print(f"Error details: {error_message}")  # Debug print
            
            if "membership_applications" in error_message.lower():
                flash('Database error: The membership applications table may not exist. Please contact support.', 'error')
            elif "membership_documents" in error_message.lower():
                flash('Storage error: Unable to upload CV file. Please try again.', 'error')
            elif "duplicate key" in error_message.lower():
                flash('You have already submitted an application with this email.', 'error')
            else:
                flash(f'An error occurred: {error_message}', 'error')
            
            return redirect(url_for('membership.OnlineApplication'))

    return render_template("screens/membership/online_appc.html")

@membership_bp.route("/list-of-life-members")
def ListOfLifeMembers():
    return render_template("screens/membership/lolm.html")