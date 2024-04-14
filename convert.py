import markdown2

# HTML section template as before
section_pic_middle_template = '''
<section data-transition="convex" data-background="assets/scroll.jpg" data-background-color="lightblue" class="scrollable top">
    <h2>{title}</h2>
    <div class="r-hstack">
        <img width="600" height="300" src="{image_src}" >
    </div>
    <h3>{subtitle}</h3>
    <div class="eli-column">
        <ul>
            {items}
        </ul>
    </div>
</section>
'''
section_pic_middle_template = '''
<section data-transition="convex" data-background="assets/scroll.jpg" data-background-color="lightblue" class="scrollable top">
    <h2>{title}</h2>
    <div class="r-hstack">
        <img width="600" height="300" src="{image_src}" >
    </div>
    <h3>{subtitle}</h3>
    <div class="eli-column">
        <ul>
            {items}
        </ul>
    </div>
</section>
'''


def markdown_to_html_list(markdown_text):
    html_content = markdown2.markdown(markdown_text)
    html_content = html_content.replace('<ul>', '').replace('</ul>', '')
    return html_content.strip()

def process_markdown_file(file_path):
    sections_html = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        sections = content.split('\n\n')
        
        for section in sections:
            parts = section.split('\n', 1)
            title = parts[0].strip('# ')
            subtitle = ''
            items = ''
            image_src = "assets/seed-of-faith-sower.jpg"
            
            if len(parts) > 1:
                if '\n-' in parts[1]:
                    items = markdown_to_html_list(parts[1])
                else:
                    subtitle = parts[1]
                    
            section_html = section_template.format(title=title, subtitle=subtitle, items=items, image_src=image_src)
            sections_html.append(section_html)
            
    return '\n'.join(sections_html)

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



# Process the markdown file to get the HTML content
content_html = process_markdown_file('out/what_is_perseverance.md')
# Insert the content into the template and save the output
insert_content_into_template(content_html, 'out/template.html', 'out/output.html')
