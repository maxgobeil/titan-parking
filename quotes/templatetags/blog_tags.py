import re

from django import template
from django.template.defaultfilters import stringfilter
from django.templatetags.static import static

register = template.Library()


@register.filter
@stringfilter
def process_blog_images(content):
    """
    Process image placeholders in blog content and convert them to HTML img tags
    Format: [image:filename.jpg|alt text|width,height|class1 class2]

    Parameters:
    - filename: required
    - alt text: optional
    - width,height: optional (one or both, comma separated)
    - classes: optional (space separated)
    """
    # Pattern to match [image:filename.jpg|alt text|width,height|class1 class2]
    pattern = r"\[image:([\w\.-]+)(?:\|(.*?))?(?:\|([\d,]+))?(?:\|([\w\s-]+))?\]"

    def replace_image(match):
        filename = match.group(1)
        alt_text = match.group(2) or filename
        size_param = match.group(3) or ""
        css_classes = match.group(4) or ""

        # Handle size parameters (width,height)
        style = ""
        if size_param:
            dimensions = size_param.split(",")
            if len(dimensions) == 1 and dimensions[0]:
                style = f"width: {dimensions[0]}px;"
            elif len(dimensions) >= 2:
                if dimensions[0] and dimensions[1]:
                    style = f"width: {dimensions[0]}px; height: {dimensions[1]}px;"
                elif dimensions[0]:
                    style = f"width: {dimensions[0]}px;"
                elif dimensions[1]:
                    style = f"height: {dimensions[1]}px;"

        # Combine default class with any user-specified classes
        all_classes = f"blog-content-image {css_classes}".strip()

        # Create the image HTML with proper static URL
        image_url = static("images/" + filename)
        style_attr = f' style="{style}"' if style else ""
        return f'<img src="{image_url}" alt="{alt_text}" class="{all_classes}"{style_attr}>'

    # Replace all instances of the pattern
    processed_content = re.sub(pattern, replace_image, content)
    return processed_content


# [image:handicap-stencil.png|Handicap Parking Stencil]
# [image:handicap-stencil.png|Handicap Stencil|400]
# [image:handicap-stencil.png|Handicap Stencil|400,300]
# [image:handicap-stencil.png|Handicap Stencil||float-left]
# [image:handicap-stencil.png|Handicap Stencil|400,300|float-left shadow]
