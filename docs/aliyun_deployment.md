# Deployment on Alibaba Cloud Linux 3 (ECS)

This guide helps you deploy EduDigest on an Alibaba Cloud ECS instance running **Alibaba Cloud Linux 3**.

## 1. Prepare the ECS Instance

Ensure your Security Group allows inbound traffic on:
- **Port 22 (SSH)**
- **Port 5000** (or 80/443 if using a reverse proxy)

## 2. Install System Dependencies

Alibaba Cloud Linux 3 uses `yum` or `dnf` (compatible with RHEL/CentOS).

```bash
# Update and install Python, Git, and development tools
sudo yum update -y
sudo yum install -y python3 python3-pip git gcc python3-devel

# Install FFmpeg (using the official static build for reliability)
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar xvf ffmpeg-release-amd64-static.tar.xz
sudo mv ffmpeg-*-amd64-static/ffmpeg /usr/local/bin/
sudo mv ffmpeg-*-amd64-static/ffprobe /usr/local/bin/
rm -rf ffmpeg-*-amd64-static*

# Verify FFmpeg
ffmpeg -version

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
pip install --upgrade pip
pip install -r requirements.txt

# Set Environment Variables
export GEMINI_API_KEY='your_api_key_here'
```

## 4. Run with Gunicorn (Production)

```bash
gunicorn --bind 0.0.0.0:5000 src.backend.app:app
```

## 5. Run as a Service (systemd)

To keep the app running in the background:

```bash
sudo vi /etc/systemd/system/edudigest.service
```

Paste the following (replace `root` if you use a different user):

```ini
[Unit]
Description=Gunicorn instance to serve EduDigest
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/edudigest
Environment="PATH=/root/edudigest/venv/bin:/usr/local/bin"
Environment="GEMINI_API_KEY=your_api_key_here"
ExecStart=/root/edudigest/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 src.backend.app:app

[Install]
WantedBy=multi-user.target
```

Then start it:
```bash
sudo systemctl daemon-reload
sudo systemctl start edudigest
sudo systemctl enable edudigest
```
