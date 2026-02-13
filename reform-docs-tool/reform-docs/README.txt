HOW TO USE THIS TOOL
============================================================

FIRST TIME ONLY
---------------
1. Double-click SETUP.bat
   This installs one small required package and creates your folders.

2. Enable GitHub Pages on your repo:
   - Go to https://github.com/alexreports/reform-docs
   - Click Settings (top right of the repo)
   - Click Pages (left sidebar)
   - Under "Source" select "Deploy from a branch"
   - Set Branch to: main   Folder to: /docs
   - Click Save

EVERYDAY USE
------------
1. Put your .md files in the CONTENT folder
2. Double-click RUN.bat
3. That's it - your site updates automatically

YOUR FOLDER STRUCTURE
---------------------
reform-docs/
  content/          <-- PUT YOUR .MD FILES HERE
    topic/
      subtopic/
        page.md
  docs/             <-- Generated HTML (do not edit manually)
  memory/           <-- State tracking (do not edit or delete)
  convert.py        <-- The main script (do not edit)
  RUN.bat           <-- Double-click this to publish
  SETUP.bat         <-- Run this once at the beginning

HOW THE MEMORY SYSTEM WORKS
----------------------------
Every time you run the tool, it checks a fingerprint of each
file stored in the memory folder. If a file has not changed,
it skips it. Only new or edited files get converted and pushed.
The memory folder mirrors your content folder structure exactly.

EXAMPLE CONTENT STRUCTURE
--------------------------
content/
  services/
    web-design/
      overview.md        becomes --> docs/services/web-design/overview.html
  about/
    team.md              becomes --> docs/about/team.html
  contact.md             becomes --> docs/contact.html

MARKDOWN BASICS
---------------
# Heading 1
## Heading 2
**bold text**
*italic text*
[link text](https://url.com)
- bullet point
1. numbered list

YOUR LIVE SITE
--------------
Once GitHub Pages is enabled your site will be live at:
https://alexreports.github.io/reform-docs/
