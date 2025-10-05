import markdown2
from PIL import Image
import os
main_title=""
# HTML section template as before
section_middle_template = '''
<section data-transition="convex" data-background="assets/scroll.jpg" data-background-color="lightblue" class="scrollable top">
    <h2>{title}</h2>
    <div class="r-hstack">
        <img width="600" height="300" src="{image_src}" >
    </div>
    <h3>{subtitle}</h3>
    <div class="eli-column">
        <{list_tag}>
            {items}
        </{list_tag}>
    </div>
</section>
'''
section_text_only_template='''
<section data-background="assets/nov/100114.jpg" data-background-color="lightblue" class="scrollable top">
    <h2>{title}</h2>
    <div class="eli-column">
        <{list_tag}>
            {items}
        </{list_tag}>
    </div>
</section>
'''
# Template for horizontal images (image on top)
section_horizontal_image_template = '''
<section data-transition="convex" data-background="assets/scroll.jpg" data-background-color="lightblue" class="scrollable top">
    <h2>{title}</h2>
    <div class="r-hstack">
        <img width="600" height="300" src="{image_src}" >
    </div>
    <h3>{subtitle}</h3>
    <div class="eli-column">
        <{list_tag}>
            {items}
        </{list_tag}>
    </div>
</section>
'''

# Template for vertical images (image on left, text on right)
section_vertical_image_template = '''
<section data-transition="convex" data-background="assets/scroll.jpg" data-background-color="lightblue" class="scrollable top">
    <h2>{title}</h2>
    <div class="r-hstack">
        <div class="r-vstack" style="flex: 1;">
            <img width="400" height="500" src="{image_src}" >
        </div>
        <div class="r-vstack" style="flex: 1;">
            <h3>{subtitle}</h3>
            <div class="eli-column">
                <{list_tag}>
                    {items}
                </{list_tag}>
            </div>
        </div>
    </div>
</section>
'''

# Template for two side-by-side images
section_two_images_template = '''
<section data-transition="convex" data-background="assets/scroll.jpg" data-background-color="lightblue" class="scrollable top">
    <h2>{title}</h2>
    <div class="r-hstack">
        <img width="400" height="300" src="{image_src1}" style="margin-right: 20px;">
        <img width="400" height="300" src="{image_src2}" style="margin-left: 20px;">
    </div>
    <h3>{subtitle}</h3>
    <div class="eli-column">
        <{list_tag}>
            {items}
        </{list_tag}>
    </div>
</section>
'''

# Template for sections with tables
section_table_template = '''
<section data-background="assets/nov/100114.jpg" data-background-color="lightblue" class="scrollable top">
    <h2>{title}</h2>
    <div class="eli-column">
        {table_content}
    </div>
</section>
'''


def get_image_aspect_ratio(image_path):
    """
    Returns 'horizontal' if width > height, 'vertical' otherwise
    """
    try:
        # Try the path as given first
        full_path = image_path
        if not os.path.exists(full_path):
            # If not found, try prepending 'out/'
            full_path = f'out/{image_path}'
        
        if os.path.exists(full_path):
            with Image.open(full_path) as img:
                width, height = img.size
                return 'horizontal' if width > height else 'vertical'
        else:
            # If image doesn't exist, assume horizontal as default
            return 'horizontal'
    except Exception:
        # If we can't determine aspect ratio, default to horizontal
        return 'horizontal'

def is_markdown_table(text):
    """
    Detect if text contains a markdown table
    """
    lines = text.strip().split('\n')
    if len(lines) < 2:
        return False
    
    # Check for table structure: header row with |, separator row with |, and at least one data row
    for i, line in enumerate(lines):
        if '|' in line:
            # Found a line with pipes, check if next line is separator
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                # Separator line should contain | and - characters
                if '|' in next_line and '-' in next_line:
                    return True
    return False

def markdown_table_to_html(markdown_text):
    """
    Convert markdown table to HTML table
    """
    lines = [line.strip() for line in markdown_text.strip().split('\n') if line.strip()]
    if len(lines) < 2:
        return ""
    
    html_parts = ['<table class="reveal-table">']
    
    # Process header row
    header_row = lines[0]
    header_cells = [cell.strip() for cell in header_row.split('|') if cell.strip()]
    if header_cells:
        html_parts.append('<thead><tr>')
        for cell in header_cells:
            html_parts.append(f'<th>{cell}</th>')
        html_parts.append('</tr></thead>')
    
    # Skip separator row (lines[1]) and process data rows
    if len(lines) > 2:
        html_parts.append('<tbody>')
        for line in lines[2:]:
            if '|' in line:
                data_cells = [cell.strip() for cell in line.split('|') if cell.strip()]
                if data_cells:
                    html_parts.append('<tr>')
                    for cell in data_cells:
                        html_parts.append(f'<td>{cell}</td>')
                    html_parts.append('</tr>')
        html_parts.append('</tbody>')
    
    html_parts.append('</table>')
    return '\n'.join(html_parts)

def convert_bold_markdown(text):
    """Convert **text** to <strong>text</strong>"""
    import re
    return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)

def markdown_to_html_list(markdown_text):
    import re
    
    lines = markdown_text.strip().split('\n')
    html_parts = []
    has_numbered_items = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for numbered list items (1. 2. etc.)
        numbered_match = re.match(r'^(\d+)\.\s+(.+)$', line)
        # Check for dash list items (- text)
        dash_match = re.match(r'^-\s+(.+)$', line)
        
        if numbered_match:
            has_numbered_items = True
            number = numbered_match.group(1)
            content = convert_bold_markdown(numbered_match.group(2))
            # Use custom styling to show the number
            html_parts.append(f'<li class="fragment numbered-item" data-number="{number}">{content}</li>')
            
        elif dash_match:
            content = convert_bold_markdown(dash_match.group(1))
            html_parts.append(f'<li class="fragment dash-item">{content}</li>')
        else:
            # Regular text, treat as list item
            content = convert_bold_markdown(line)
            html_parts.append(f'<li class="fragment">{content}</li>')
    
    html_content = '\n'.join(html_parts)
    
    return html_content.strip(), has_numbered_items

def process_markdown_file(file_path):
    sections_html = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        sections = content.split('\n\n')
        
        for section in sections:
            section = section.lstrip('\n')
            #remove any empty string in the list 


            if section=="":
                continue
            parts = section.split('\n', 1)
            parts = list(filter(None, parts))
            if parts[0][:2]=="# ":
                parts[0]= parts[0].replace("#","")
                main_title = parts[0]
                continue
            if parts[0]=="" or parts[0]=="\n":
                list_temp = parts[1:]
                parts=list_temp
                continue
            if len(parts) > 1 and parts[1][0]=="`":
                title = parts[0].strip('# ')
                parts = parts[1].split('`\n')
                subtitle = ''
                items = ''
                
                # Extract image paths - handle multiple images on the same line
                image_line = parts[0].replace('`','')
                image_paths = [path.strip() for path in image_line.split() if path.strip()]
                
                if len(parts) > 1:
                    if '\n-' in parts[1]:
                        items, is_ordered = markdown_to_html_list(parts[1])
                        list_tag = 'ol' if is_ordered else 'ul'
                    elif parts[1][:2]=="##":
                        subtitle = parts[1]
                        items = ''
                        list_tag = 'ul'
                    else:
                        items, is_ordered = markdown_to_html_list(parts[1])
                        list_tag = 'ol' if is_ordered else 'ul'
                else:
                    items = ''
                    list_tag = 'ul'
                
                # Choose template based on number of images and aspect ratio
                if len(image_paths) == 2:
                    # Two images side by side
                    section_html = section_two_images_template.format(
                        title=title, 
                        subtitle=subtitle, 
                        items=items, 
                        image_src1=image_paths[0],
                        image_src2=image_paths[1],
                        list_tag=list_tag
                    )
                elif len(image_paths) == 1:
                    # Single image - check aspect ratio
                    aspect_ratio = get_image_aspect_ratio(image_paths[0])
                    if aspect_ratio == 'horizontal':
                        section_html = section_horizontal_image_template.format(
                            title=title, 
                            subtitle=subtitle, 
                            items=items, 
                            image_src=image_paths[0], 
                            list_tag=list_tag
                        )
                    else:  # vertical
                        section_html = section_vertical_image_template.format(
                            title=title, 
                            subtitle=subtitle, 
                            items=items, 
                            image_src=image_paths[0], 
                            list_tag=list_tag
                        )
                else:
                    # Fallback to original template if no images or more than 2
                    section_html = section_middle_template.format(
                        title=title, 
                        subtitle=subtitle, 
                        items=items, 
                        image_src=image_paths[0] if image_paths else '', 
                        list_tag=list_tag
                    )
                
                sections_html.append(section_html)
            else:
                title = parts[0].strip('#-text- ')
                if len(parts) > 1:
                    # Check if content contains a table
                    if is_markdown_table(parts[1]):
                        table_content = markdown_table_to_html(parts[1])
                        section_html = section_table_template.format(title=title, table_content=table_content)
                    else:
                        items, is_ordered = markdown_to_html_list(parts[1])
                        list_tag = 'ol' if is_ordered else 'ul'
                        section_html = section_text_only_template.format(title=title, items=items, list_tag=list_tag)
                else:
                    items = ''
                    list_tag = 'ul'
                    section_html = section_text_only_template.format(title=title, items=items, list_tag=list_tag)
                sections_html.append(section_html)
    return '\n'.join(sections_html),main_title

def insert_content_into_template(content, template_path, output_path):
    with open(template_path, 'r', encoding='utf-8') as file:
        template = file.read()
        
    # Locate the position where to insert the content within the "slides" div
    insertion_point = template.find('<div class="slides">') + len('<div class="slides">')
    
    # Check if the insertion point was found
    if insertion_point > len('<div class="slides">'):
        # Split the template at the insertion point and insert the content
        part_one = template[:insertion_point]
        part_two = template[insertion_point:]
        final_html = f'{part_one}\n{content}\n{part_two}'
    else:
        # If the "slides" div wasn't found, keep the template unchanged (or handle the error as needed)
        final_html = template
        print("Error: Could not find the 'slides' div in the template.")
    
    # Save the modified template with the inserted content
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(final_html)

def insert_title_into_the_html(content_html,main_title):
    with open(f'out/{md_name}.html', 'r', encoding='utf-8') as file:
        template = file.read()
    insertion_point = template.find('		<title>') + len('		<title>')
    if insertion_point > len('<h1 class="title">'):
        part_one = template[:insertion_point]
        part_two = template[insertion_point:]
        final_html = f'{part_one}\n{main_title}\n{part_two}'
    else:
        final_html = template
        print("Error: Could not find the 'title' div in the template.")
    with open(f'out/{md_name}.html', 'w', encoding='utf-8') as file:
        file.write(final_html)

md_name="05102025_west_short_q1_q3"
# Process the markdown file to get the HTML content
content_html,main_title = process_markdown_file(f'out/{md_name}.md')
# Insert the content into the template and save the output
insert_content_into_template(content_html, 'out/template.html', f'out/{md_name}.html')
insert_title_into_the_html('out/template.html',main_title)