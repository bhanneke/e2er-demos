import sys
from pathlib import Path

sys.path.insert(0, "/tmp/e2er-demos/uvtools/e2er/lib/python3.14/site-packages")
from src.core.renderer.figures import render_figures

report = render_figures(Path(".").resolve())
print("rendered:", getattr(report, "rendered", report))
print("errors:", getattr(report, "errors", None))
