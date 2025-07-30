# FBCommentX

🚀 **FBCommentX** is a Python automation tool that uses Selenium to log into Facebook and automatically post comments on specified posts. It is designed for developers, testers, and marketers who need to automate comment posting on Facebook for engagement or testing purposes.

> ⚠️ This tool is intended for educational and research use only. Use responsibly and in compliance with Facebook's Terms of Service.

---

## 📌 Features

- Login automation with email and password
- Commenting on any public or accessible Facebook post
- Multiple comment posting logic
- Headless browsing support (no GUI)
- Configurable via command-line arguments
- Basic cookie acceptance and anti-checkpoint handling

---

## 🔧 Requirements

- Python 3.6+
- Google Chrome installed
- ChromeDriver compatible with your Chrome version
```bash
Set ChromeDriver path (optional)
Download and place the ChromeDriver binary in a known location.
```

---

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/IlyassCODEX/FBCommentX.git
cd FBCommentX
pip install -r requirements.txt
python3 cs.py
```

---

Usage :

```bash
python3 cs.py \
  --email your_email@example.com(or phone number) \
  --password your_password \
  --post-url https://www.facebook.com/yourtargetpost \
  --comment "This is my automated comment!" \
  --chromedriver-path /path/to/chromedriver \
  --headless
```
