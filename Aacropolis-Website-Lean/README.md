# Aacropolis Homes

Upload this folder’s contents to your repository root. In GitHub Pages, select `main` and `/ (root)`.

The HTML files work as supplied—no installation needed.

To edit and rebuild:
- Page content: `tools/pages.json`
- Styling: `assets/site.css`
- Map locations: `assets/build-map/locations.json`
- Rebuild: `python3 tools/build.py`
- Check links: `python3 tools/check.py`

Booking links use the existing Aacropolis website. Map tiles require internet access. If using another repository, update `SITE_URL` in `tools/build.py` and rebuild.
