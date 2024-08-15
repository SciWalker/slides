import markdown2
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
        <ul>
            {items}
        </ul>
    </div>
</section>
'''
section_text_only_template='''
<section data-markdown data-background="assets/nov/100114.jpg" data-background-color="lightblue"  class="scrollable top">
  <script type="text/template">
    ## {title}
    {items}

  </script>
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
            
            if parts[0][:2]=="# ":
                parts[0]= parts[0].replace("#","")
                main_title = parts[0]
                print(main_title)
                continue
            if parts[1][0]=="`":
                title = parts[0].strip('# ')
                parts = parts[1].split('`\n')
                subtitle = ''
                items = ''
                image_src = parts[0].replace('`','')
                if len(parts) > 1:
                    if '\n-' in parts[1]:
                        items = markdown_to_html_list(parts[1])
                    elif parts[1][:2]=="##":
                        subtitle = parts[1]
                        
                section_html = section_middle_template.format(title=title, subtitle=subtitle, items=items, image_src=image_src)
                sections_html.append(section_html)
            else:
                title = parts[0].strip('#-text- ')
                items = parts[1]
                section_html = section_text_only_template.format(title=title, items=items)
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

md_name="lord's_prayer"
# Process the markdown file to get the HTML content
content_html,main_title = process_markdown_file(f'out/{md_name}.md')
# Insert the content into the template and save the output
insert_content_into_template(content_html, 'out/template.html', f'out/{md_name}.html')
insert_title_into_the_html('out/template.html',main_title)