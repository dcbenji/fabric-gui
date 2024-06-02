import markdown
import subprocess

def copy_raw_markdown(text):
    pyperclip.copy(text)

def render_markdown(text):
    return markdown.markdown(text)

def copy_raw_markdown(text):
    process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    process.communicate(text.encode('utf-8'))