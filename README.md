# Image Harvest Setup Instructions

## Installation

### For Windows

1. **Download Python:**

   - Go to the [official Python download page for Windows](https://www.python.org/downloads/windows/).
   - Download the Python 3 release.
   - Run the executable installer. For more info, refer to the link above.

2. **Install Image Harvest:**
   - [Download Image Harvest](#link-to-download) (Link needed).
   - Navigate to the download folder and execute `Install-Package.bat`.
   - Input credentials in `credentials.py`.
   - Run Image Harvest by executing the application.

### For Mac

1. **Using Installer:**

   - Go to the [official Python download page for Mac](https://www.python.org/downloads/mac-osx/).
   - Download and run the installer.

2. **Using Homebrew:**
   - Open your terminal.
   - Install Homebrew by executing:
     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
   - Input your password.
   - Install pyenv using Homebrew:
     ```bash
     brew install pyenv
     ```
   - Update Python with pyenv:
     ```bash
     pyenv install 3.9.2
     ```

## Using Image Harvest

1. **Scrape Images:**
   - Copy the desired URL of the website from which you need to scrape images.
   - Open Image Harvest application.
   - Enter the URL and specify the maximum number of images to scrape.
   - Wait for the images to be downloaded.
   - Downloaded images will be stored in their respective folders.
