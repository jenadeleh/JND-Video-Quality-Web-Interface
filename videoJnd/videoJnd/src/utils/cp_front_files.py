import os
from pathlib import Path
import shutil

if __name__ == "__main__":

    js_path = Path("../../static/js/")
    css_path = Path("../../static/css/")
    html_path = Path("../../templates/")

    dist_path = Path("../../../../GUI/dist/")

    with open(dist_path / "index.html", "r") as fi:
        html = fi.read()
        html = html.replace(
            """<script type="text/javascript" src="bundle.js"></script></body>""",
            """<script type="text/javascript" src="../static/js/bundle.js"></script></body>"""
        )

    with open(dist_path / "index.html", "w") as fi:
        fi.write(html)

    with open(dist_path / "bundle.js", "r") as fi:
        bundle = fi.read()
        bundle = bundle.replace(
            "http://127.0.0.1:8000/scheduler",
            "/scheduler"
        )    

    with open(dist_path / "bundle.js", "w") as fi:
        fi.write(bundle)

    shutil.copy(dist_path / "bundle.js", js_path / "bundle.js")
    shutil.copy(dist_path / "bundle.js.map", js_path / "bundle.js.map")
    shutil.copy(dist_path / "css/style.css", css_path / "style.css")
    shutil.copy(dist_path / "index.html", html_path / "index.html")




