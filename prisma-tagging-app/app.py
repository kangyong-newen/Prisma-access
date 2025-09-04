from flask import Flask, render_template, send_file, Response, request, jsonify
import qrcode, io, jwt, time

app = Flask(__name__)

# 태깅 토큰용 비밀키
TAGGING_SECRET = "your-super-secret-key"

# 내부망 공인 IP 기준
INTERNAL_IP = "211.58.74.253"

# 메인 페이지
@app.route("/")
def index():
    return render_template("index.html")

# 인증 완료 페이지
@app.route("/complete")
def complete():
    return render_template("complete.html")

# 태깅 토큰 생성 API
@app.route("/get-tag-token", methods=["POST"])
def get_tag_token():
    client_ip = request.json.get("ip")  # 클라이언트가 보고한 IP
    xff_raw = request.headers.get("X-Forwarded-For", request.remote_addr)

    # XFF가 여러 IP일 경우 첫 번째 IP만 사용
    xff_ip = xff_raw.split(",")[0].strip() if "," in xff_raw else xff_raw

    # 내부망 판단: XFF IP가 내부망 기준과 일치하면 internal
    tag = "internal" if xff_ip == INTERNAL_IP else "external"

    payload = {
        "ip": client_ip,
        "xff_ip": xff_ip,
        "tag": tag,
        "origin": "user.cloude.co.kr",
        "exp": time.time() + 30
    }
    token = jwt.encode(payload, TAGGING_SECRET, algorithm="HS256")

    print(f"[TAGGING] client_ip={client_ip}, xff_ip={xff_ip}, tag={tag}")
    return jsonify({ "token": token, "tag": tag })

# iOS용 .mobileconfig 다운로드
@app.route("/download-profile")
def download_profile():
    return send_file(
        "ssl-profile.mobileconfig",
        mimetype="application/x-apple-aspen-config",
        as_attachment=True,
        download_name="ssl-profile.mobileconfig"
    )

# Android용 인증서 다운로드
@app.route("/download-cert")
def download_cert():
    return send_file(
        "static/root-ca.crt",
        mimetype="application/x-x509-ca-cert",
        as_attachment=True,
        download_name="root-ca.crt"
    )

# QR 코드 생성 (iOS)
@app.route("/qr/ios")
def qr_ios():
    url = request.host_url.rstrip("/") + "/download-profile"
    qr_img = qrcode.make(url)
    buf = io.BytesIO()
    qr_img.save(buf, format='PNG')
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')

# QR 코드 생성 (Android)
@app.route("/qr/android")
def qr_android():
    url = request.host_url.rstrip("/") + "/download-cert"
    qr_img = qrcode.make(url)
    buf = io.BytesIO()
    qr_img.save(buf, format='PNG')
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')

# QR 선택 페이지
@app.route("/show-qr")
def show_qr():
    return render_template("qr.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)