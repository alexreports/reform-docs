"""
MD to HTML Converter with GitHub Push
Converts changed Markdown files to HTML and pushes to GitHub Pages
"""

import os
import hashlib
import shutil
import subprocess
import sys
import datetime

try:
    import markdown
except ImportError:
    print("Installing required package...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown"])
    import markdown

# ── Folder configuration ──────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(BASE_DIR, "content")   # your .md files go here
OUTPUT_DIR  = os.path.join(BASE_DIR, "docs")       # GitHub Pages serves this
MEMORY_DIR  = os.path.join(BASE_DIR, "memory")     # state tracking
# ─────────────────────────────────────────────────────────────────────────────

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Georgia, 'Times New Roman', serif;
            max-width: 860px;
            margin: 60px auto;
            padding: 0 24px;
            color: #1a1a1a;
            line-height: 1.75;
            background: #fff;
        }}
        h1, h2, h3, h4 {{
            font-family: Arial, Helvetica, sans-serif;
            font-weight: 700;
            color: #111;
            margin-top: 2em;
            line-height: 1.3;
        }}
        h1 {{ font-size: 2em; border-bottom: 2px solid #e0e0e0; padding-bottom: 0.3em; }}
        h2 {{ font-size: 1.5em; }}
        h3 {{ font-size: 1.2em; }}
        a {{ color: #0056b3; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.9em;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background: #f4f4f4;
            padding: 16px;
            border-radius: 4px;
            overflow-x: auto;
        }}
        pre code {{
            background: none;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #ccc;
            margin-left: 0;
            padding-left: 20px;
            color: #555;
        }}
        img {{ max-width: 100%; height: auto; }}
        table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: left; }}
        th {{ background: #f4f4f4; font-weight: bold; }}
        .site-footer {{
            margin-top: 60px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            font-size: 0.85em;
            color: #888;
            font-family: Arial, Helvetica, sans-serif;
        }}
    </style>
</head>
<body>
{body}
<div class="site-footer">Last updated: {date}</div>
</body>
</html>"""


def get_file_hash(filepath):
    """Return MD5 hash of a file's contents."""
    with open(filepath, "r", encoding="utf-8") as f:
        return hashlib.md5(f.read().encode()).hexdigest()


def get_memory_path(md_path):
    """Return the memory file path that mirrors the content path."""
    relative = os.path.relpath(md_path, CONTENT_DIR)
    return os.path.join(MEMORY_DIR, relative + ".hash")


def get_output_path(md_path):
    """Return the output HTML path that mirrors the content path."""
    relative = os.path.relpath(md_path, CONTENT_DIR)
    html_relative = os.path.splitext(relative)[0] + ".html"
    return os.path.join(OUTPUT_DIR, html_relative)


def has_changed(md_path):
    """Return True if the file is new or has changed since last run."""
    memory_path = get_memory_path(md_path)
    if not os.path.exists(memory_path):
        return True
    with open(memory_path, "r") as f:
        saved_hash = f.read().strip()
    return saved_hash != get_file_hash(md_path)


def save_memory(md_path):
    """Save the current hash of a file to memory."""
    memory_path = get_memory_path(md_path)
    os.makedirs(os.path.dirname(memory_path), exist_ok=True)
    with open(memory_path, "w") as f:
        f.write(get_file_hash(md_path))


def convert_file(md_path):
    """Convert a single Markdown file to HTML."""
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Convert markdown to HTML
    md_extensions = ["tables", "fenced_code", "toc", "nl2br"]
    html_body = markdown.markdown(md_content, extensions=md_extensions)

    # Extract title from first H1 or use filename
    title = os.path.splitext(os.path.basename(md_path))[0].replace("-", " ").replace("_", " ").title()
    for line in md_content.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break

    today = datetime.date.today().strftime("%B %d, %Y")
    full_html = HTML_TEMPLATE.format(title=title, body=html_body, date=today)

    output_path = get_output_path(md_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    return output_path


def build_index():
    """Generate a simple index.html listing all pages."""
    links = []
    for root, dirs, files in os.walk(OUTPUT_DIR):
        dirs.sort()
        for fname in sorted(files):
            if fname.endswith(".html") and fname != "index.html":
                full_path = os.path.join(root, fname)
                rel = os.path.relpath(full_path, OUTPUT_DIR).replace("\\", "/")
                label = os.path.splitext(fname)[0].replace("-", " ").replace("_", " ").title()
                folder = os.path.relpath(root, OUTPUT_DIR)
                if folder == ".":
                    folder = "Root"
                links.append((folder, label, rel))

    if not links:
        return

    items_html = ""
    current_folder = None
    for folder, label, href in links:
        if folder != current_folder:
            if current_folder is not None:
                items_html += "</ul>\n"
            items_html += f"<h2>{folder}</h2>\n<ul>\n"
            current_folder = folder
        items_html += f'  <li><a href="{href}">{label}</a></li>\n'
    if current_folder is not None:
        items_html += "</ul>\n"

    today = datetime.date.today().strftime("%B %d, %Y")
    index_html = HTML_TEMPLATE.format(
        title="Site Index",
        body=f"<h1>Site Index</h1>\n{items_html}",
        date=today
    )
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print("  Updated index.html")


def git_push(changed_files):
    """Commit changed files and push to GitHub."""
    try:
        subprocess.run(["git", "add", "docs/", "memory/"], cwd=BASE_DIR, check=True)
        msg = f"Update {len(changed_files)} page(s) - {datetime.date.today()}"
        subprocess.run(["git", "commit", "-m", msg], cwd=BASE_DIR, check=True)
        subprocess.run(["git", "push"], cwd=BASE_DIR, check=True)
        print("\nPushed to GitHub successfully.")
    except subprocess.CalledProcessError as e:
        print(f"\nGit error: {e}")
        print("Check that you are connected to the internet and have GitHub access.")


def main():
    print("=" * 60)
    print("  MD to HTML Converter")
    print("=" * 60)

    # Make sure content folder exists
    os.makedirs(CONTENT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(MEMORY_DIR, exist_ok=True)

    # Find all markdown files
    md_files = []
    for root, dirs, files in os.walk(CONTENT_DIR):
        dirs.sort()
        for fname in sorted(files):
            if fname.endswith(".md"):
                md_files.append(os.path.join(root, fname))

    if not md_files:
        print("\nNo .md files found in the content folder.")
        print(f"Add your Markdown files to: {CONTENT_DIR}")
        input("\nPress Enter to exit.")
        return

    # Convert changed files
    changed = []
    skipped = 0
    for md_path in md_files:
        rel = os.path.relpath(md_path, CONTENT_DIR)
        if has_changed(md_path):
            print(f"  Converting: {rel}")
            convert_file(md_path)
            save_memory(md_path)
            changed.append(md_path)
        else:
            skipped += 1

    print(f"\nConverted: {len(changed)} file(s)  |  Skipped (unchanged): {skipped}")

    if changed:
        build_index()
        print("\nPushing to GitHub...")
        git_push(changed)
    else:
        print("Nothing to push - all files are up to date.")

    input("\nDone. Press Enter to close.")


if __name__ == "__main__":
    main()
