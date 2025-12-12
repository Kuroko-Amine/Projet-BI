import sys
import subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import pypdf
except ImportError:
    print("Installing pypdf...")
    install("pypdf")
    import pypdf

reader = pypdf.PdfReader('Travaille Ã  faire pour ING3 sÃ©cu.pdf')
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"
print(text)
