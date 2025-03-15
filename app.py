from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify, flash, session
import os
import asyncio
import threading
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
# from flask_mail import Mail, Message
from api.whisper_LLM_api import api

# ✅ Flask Configuration
app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["OUTPUT_FOLDER"] = "output"
app.config["ALLOWED_EXTENSIONS"] = {"mp4", "pdf"}
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ✅ Ensure Upload & Output Folders Exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["OUTPUT_FOLDER"], exist_ok=True)

# ✅ User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ✅ Check Allowed File Types
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

# ✅ Background Processing Task
def run_processing(video_path, pdf_path, num_of_pages, resolution, user_folder):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    status_file = os.path.join(user_folder, "processing.txt")

    # ✅ Mark processing as ongoing
    with open(status_file, "w") as f:
        f.write("processing")

    try:
        loop.run_until_complete(api(
            video_path=video_path,
            pdf_file_path=pdf_path,
            poppler_path="./poppler/poppler-0.89.0/bin",
            output_audio_dir=os.path.join(user_folder, 'audio'),
            output_video_dir=os.path.join(user_folder, 'video'),
            output_text_path=os.path.join(user_folder, "text_output.txt"),
            num_of_pages=num_of_pages,
            resolution=int(resolution)
        ))

        # ✅ Processing complete, remove status file
        os.remove(status_file)
        print("✅ Video Processing Completed!")
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        with open(status_file, "w") as f:
            f.write("failed")

# ✅ Home Route
@app.route("/")
def index():
    return render_template("index.html")

# ✅ Login & Signup Routes (Already Implemented)
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")

        if User.query.filter_by(email=email).first():
            flash("⚠️ Email already registered!", "error")
            return redirect(url_for("signup"))

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("✅ Account created! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("✅ Logged in successfully!", "success")
            return redirect(url_for("index"))
        else:
            flash("❌ Invalid email or password.", "error")

    return render_template("login.html")




@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("🔓 Logged out successfully.", "success")
    return redirect(url_for("index"))

# ✅ Process Video (Secure)
@app.route("/process", methods=["POST"])
@login_required
def process_video():
    user_folder = os.path.join(app.config["OUTPUT_FOLDER"], str(current_user.id))
    os.makedirs(user_folder, exist_ok=True)
    
    if request.method == 'POST':
        video_file = request.files.get("video")
        pdf_file = request.files.get("pdf")
        resolution = request.form.get("resolution")
        num_of_pages = request.form.get('num_of_pages')
    if not video_file or not pdf_file:
        return jsonify({"status": "error", "message": "⚠️ Please upload both a video and a PDF file."}), 400

    video_path = os.path.join(user_folder, secure_filename(video_file.filename))
    pdf_path = os.path.join(user_folder, secure_filename(pdf_file.filename))
    video_file.save(video_path)
    pdf_file.save(pdf_path)

    processing_thread = threading.Thread(target=run_processing, args=(video_path, pdf_path, num_of_pages, resolution, user_folder))
    processing_thread.start()

    return jsonify({"status": "success", "message": "🚀 Processing started!"}), 200

# ✅ Download Page (User Restricted)
@app.route("/download")
@login_required
def download():
    user_folder = os.path.join(app.config["OUTPUT_FOLDER"], str(current_user.id), 'video')

    # ✅ Check if processing is still ongoing
    processing_file = os.path.join(user_folder, "processing.txt")
    is_processing = os.path.exists(processing_file)

    files = []
    if os.path.exists(user_folder) and not is_processing:
        files = [f for f in os.listdir(user_folder) if f.endswith(".mp4")]

    return render_template("download.html", files=files, is_processing=is_processing)

# ✅ Secure File Download
@app.route("/download/<filename>")
@login_required
def download_file(filename):
    user_folder = os.path.join(app.config["OUTPUT_FOLDER"], str(current_user.id), 'video')

    # ✅ Ensure filename is not empty
    if not filename:
        flash("⚠️ Invalid file request!", "error")
        return redirect(url_for("download"))

    # ✅ Secure the filename and remove any unwanted spaces
    secure_file = secure_filename(filename.strip())  

    # ✅ Construct full file path
    file_path = os.path.join(user_folder, secure_file)

    # ✅ Debugging Output
    print(f"📂 Looking for: {file_path}")
    print(f"🛠️ File Exists: {os.path.exists(file_path)}")

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash("⚠️ File not found!", "error")
        return redirect(url_for("download"))


# ✅ Delete File Endpoint (User Restricted)
@app.route("/delete/<filename>", methods=["DELETE"])
@login_required
def delete_file(filename):
    try:
        user_folder = os.path.join(app.config["OUTPUT_FOLDER"], str(current_user.id), 'video')
        file_path = os.path.join(user_folder, secure_filename(filename))
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({"status": "success", "message": "File deleted successfully!"})
        else:
            return jsonify({"status": "error", "message": "File not found."}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error deleting file: {str(e)}"}), 500

# ✅ Initialize Database
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
