def markdown_to_blocks(markdown):
    new_markdown = markdown.split("\n\n")
    clean_markdown = []
    for text in new_markdown:
        if not text:
            continue
        clean_markdown.append(text.strip())
    return clean_markdown
