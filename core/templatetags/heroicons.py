from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()

# Heroicons v2 — outline (https://heroicons.com)
OUTLINE = {
    "paper-airplane": (
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5" />'
    ),
    "bars-3": (
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />'
    ),
    "x-mark": (
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M6 18 18 6M6 6l12 12" />'
    ),
    "check": (
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M4.5 12.75l6 6 9-13.5" />'
    ),
    "check-circle": (
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />'
    ),
    "banknotes": (
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M2.25 18.75a60.07 60.07 0 0 1 15.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 0 1 3 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 0 0-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 0 1-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 0 0 3 15h-.375M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm3 0h.008v.008H18V10.5Zm-12 0h.008v.008H6V10.5Z" />'
    ),
    "lifebuoy": (
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M16.712 4.33a9.027 9.027 0 0 1 1.652 1.306c.51.51.944 1.064 1.306 1.652M16.712 4.33l-3.447 3.447m3.447-3.447 3.447 3.447M6.75 19.5a9 9 0 1 0 0-18 9 9 0 0 0 0 18ZM12 13.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z" />'
    ),
    "calendar-days": (
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5m-9-6h.008v.008H12v-.008ZM12 15h.008v.008H12V15Zm0 2.25h.008v.008H12v-.008ZM9.75 15h.008v.008H9.75V15Zm0 2.25h.008v.008H9.75v-.008ZM7.5 15h.008v.008H7.5V15Zm0 2.25h.008v.008H7.5v-.008Zm6.75-4.5h.008v.008h-.008v-.008Zm0 2.25h.008v.008h-.008V15Zm0 2.25h.008v.008h-.008v-.008Zm2.25-4.5h.008v.008H16.5v-.008Zm0 2.25h.008v.008H16.5V15Z" />'
    ),
    "map-pin": (
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />'
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" />'
    ),
    "arrow-right": (
        '<path stroke-linecap="round" stroke-linejoin="round" '
        'd="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />'
    ),
}


@register.simple_tag
def heroicon(name, css_class="h-5 w-5", element_id="", aria_hidden="true"):
    """Render a Heroicons v2 outline SVG by name."""
    paths = OUTLINE.get(name)
    if not paths:
        return ""

    id_attr = format_html(' id="{}"', element_id) if element_id else ""
    aria = "true" if aria_hidden == "true" else "false"

    return mark_safe(
        f'<svg class="{css_class}" xmlns="http://www.w3.org/2000/svg" '
        f'fill="none" viewBox="0 0 24 24" stroke-width="1.5" '
        f'stroke="currentColor" aria-hidden="{aria}"{id_attr}>'
        f"{paths}</svg>"
    )
