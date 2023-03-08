import pdfkit
from flask import (Blueprint, jsonify, make_response,
                   render_template, request)
from flask_login import LoginManager, current_user, login_required

from models import Letter, User, db
from utils import (generate_cover_letter,
                   get_last_two_job_descriptions_for_user,
                   get_num_letters_for_user, letter_history)

home = Blueprint(
    "home", __name__, template_folder="./templates", static_folder="./static"
)
login_manager = LoginManager()
login_manager.init_app(home)


@home.route("/home", methods=["GET"])
@login_required
def show():
    user = User.query.filter_by(email=current_user.email).first()
    number_letter = get_num_letters_for_user(user.id)
    job_descriptions = get_last_two_job_descriptions_for_user(user.id)
    letters = letter_history(user.id)
    print(number_letter, job_descriptions)

    return render_template(
        "index.html",
        number_letter=number_letter,
        job_descriptions=job_descriptions,
        letters=letters,
    )


@home.route("/generate-pdf", methods=["GET", "POST"])
@login_required
def generate_pdf():
    if request.method == "POST":
        # Get user inputs from the form
        your_name = request.form.get("your-name", "")
        your_address = request.form.get("your-address", "")
        your_city_state_zip = request.form.get("your-city-state-zip", "")
        your_phone_number = request.form.get("your-phone-number", "")
        your_email_address = request.form.get("your-email-address", "")
        date = request.form.get("date", "")
        recipient_name = request.form.get("recipient-name", "")
        recipient_title = request.form.get("recipient-title", "")
        organization_name = request.form.get("organization-name", "")
        organization_address = request.form.get("organization-address", "")
        organization_city_state_zip = request.form.get(
            "organization-city-state-zip", ""
        )
        config = pdfkit.configuration(
            wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        )
        letters = (
            Letter.query.filter_by(user_id=current_user.id)
            .order_by(Letter.id.desc())
            .first()
        )
        content = letters.content
        # Use pdfkit to generate the PDF using a template
        rendered_template = render_template(
            "pdf.html",
            your_name=your_name,
            your_address=your_address,
            your_city_state_zip=your_city_state_zip,
            your_phone_number=your_phone_number,
            your_email_address=your_email_address,
            date=date,
            recipient_name=recipient_name,
            recipient_title=recipient_title,
            organization_name=organization_name,
            organization_address=organization_address,
            organization_city_state_zip=organization_city_state_zip,
            content=content,
        )
        pdf = pdfkit.from_string(rendered_template, False, configuration=config)

        # Create a response containing the PDF and set headers to force download
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "attachment; filename=output.pdf"
        return response

    return render_template("index.html")


@home.route("/generate", methods=["GET", "POST"])
@login_required
def generate():
    if request.method == "POST":
        job_description = request.form["job_description"]
        your_name = request.form["name"]
        company_name = request.form["company_name"]
        skills = request.form["skills"]
        user = User.query.filter_by(email=current_user.email).first()

        # cover_letter = generate_cover_letter(company_name=company_name, name=your_name, job_description=job_description, skills=skills)
        cover_letter = "Dear CoverEase,\n\nI am writing in regards to the open position for a Software Engineer. Based on the job description, I believe that my skills and experience make me the perfect candidate for the role.\n\nAs a web developer, I am well-versed in Flask, Django, HTML, CSS, and JavaScript. I have experience building and maintaining complex web applications, and am confident that I could do the same for CoverEase. In addition, I am always keeping up-to-date with the latest web development trends and technologies, so that I can provide the best possible product to my users.\n\nI would be a valuable asset to the CoverEase team, and I am eager to put my skills to work in order to help the company achieve its goals. I look forward to discussing my qualifications further with you, and thank you for your time and consideration.\n\nSincerely,\n\nNNEJI IFEANYI DANIEL"
        if user:
            letter = Letter(
                content=cover_letter,
                skills=skills,
                company_name=company_name,
                job_description=job_description,
                user=user,
            )
            db.session.add(letter)
            db.session.commit()
        else:
            pass

        return jsonify({"cover_letter": cover_letter})

    return render_template(
        "index.html", num_letter=get_num_letters_for_user(current_user.id)
    )
