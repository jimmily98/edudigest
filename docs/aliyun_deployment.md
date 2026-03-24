# Deployment on Alibaba Cloud (ECS)

This guide helps you deploy EduDigest on your existing Alibaba Cloud ECS instance.

## 1. Prepare the ECS Instance

Ensure your Security Group allows inbound traffic on:
- **Port 22 (SSH)**
- **Port 5000** (or 80 if using a reverse proxy like Nginx)

## 2. Install System Dependencies

Connect to your ECS via SSH and run:

```bash
# Update and install Python + FFmpeg
sudo apt update
sudo apt install -y python3-pip python3-venv ffmpeg git

# Clone the repository
git clone https://github.com/jimmily98/edudigest.git
cd edudigest
```

## 3. Set Up the Application

```bash
# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set Environment Variables
export GEMINI_API_KEY='your_api_key_here'
```

## 4. Run with Gunicorn (Production)

Instead of the development server, use Gunicorn for stability:

```bash
gunicorn --bind 0.0.0.0:5000 src.backend.app:app
```

## 5. (Optional) Run as a Service

To keep the app running in the background, create a systemd service:

```bash
sudo nano /etc/systemd/system/edudigest.service
```

Paste the following (adjust paths to match your ECS user):

```ini
[Unit]
Description=Gunicorn instance to serve EduDigest
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/edudigest
Environment="PATH=/root/edudigest/venv/bin"
Environment="GEMINI_API_KEY=your_api_key_here"
ExecStart=/root/edudigest/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 src.backend.app:app

[Install]
WantedBy=multi-user.target
```

Then start it:
```bash
sudo systemctl start edudigest
sudo systemctl enable edudigest
```
