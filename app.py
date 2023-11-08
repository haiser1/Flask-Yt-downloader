from flask import Flask, flash,render_template, request, url_for, redirect, send_file, session
from pytube import YouTube
from io import BytesIO

app = Flask(__name__)
app.config['SECRET_KEY'] = "654c0fb3968af9d5e6a9b3edcbc7051b"

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        session['link'] = request.form.get('url')
        try:
            url = YouTube(session['link'])
            url.check_availability()
        except:
            flash('Link Tidak Valid', 'danger')
            return redirect(url_for('home'))
        return render_template("download.html", url = url)
    return render_template("index.html")

@app.route("/download", methods = ["GET", "POST"])
def download_video():
    try:
        if request.method == "POST":
            buffer = BytesIO()
            url = YouTube(session['link'])
            itag = request.form.get("itag")
            video = url.streams.get_by_itag(itag)
            video.stream_to_buffer(buffer)
            buffer.seek(0)
            return send_file(buffer, as_attachment=True, download_name=f"{url.title}", mimetype="video/mp4")
    except:
        flash('Maaf Video Tidak Dapat Didownload', 'danger')
        return redirect(url_for('home'))
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')