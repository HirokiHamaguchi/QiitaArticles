import pyperclip


def convertMathBlocks(inputFile, outputFile):
    try:
        with open(inputFile, "r", encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: The file {inputFile} does not exist.")

    lines = content.splitlines()
    assert lines[0].startswith("# ")
    assert lines[1].strip() == ""
    lines = lines[2:]

    convertedLines = [
        "<!-- markdownlint-disable MD041 -->",
        "",
    ]
    mathBlockOpen = False
    nextIgnore = False

    for line in lines:
        if line.strip() == "$$":
            if not mathBlockOpen:
                convertedLines.append("\n```math")
                mathBlockOpen = True
            else:
                convertedLines.append("```\n")
                mathBlockOpen = False
        elif line.strip() == "> $$":
            if not mathBlockOpen:
                convertedLines.append(">")
                convertedLines.append("> ```math")
                mathBlockOpen = True
            else:
                convertedLines.append("> ```")
                convertedLines.append(">")
                mathBlockOpen = False
        elif line.startswith("!["):
            if nextIgnore:
                convertedLines.append(line)
                nextIgnore = False
                continue
            # ![alt](url) -> <img width=100% src="url" alt="alt">
            alt = line[line.find("[") + 1 : line.find("]")]
            url = line[line.find("(") + 1 : line.find(")")]
            convertedLines.append(f'<img width=100% src="{url}" alt="{alt}">')
        elif line.strip() == "<!-- ignore -->":
            nextIgnore = True
            continue
        else:
            convertedLines.append(line)

    convertedContent = "\n".join(convertedLines) + "\n"

    convertedContent = convertedContent.replace("\n\n\n", "\n\n")
    convertedContent = convertedContent.replace("\n\n\n", "\n\n")
    convertedContent = convertedContent.replace("\n\n\n", "\n\n")

    with open(outputFile, "w", encoding="utf-8") as file:
        file.write(convertedContent)

    print(f"Conversion completed successfully. Output saved to {outputFile}")


def main():
    inputFile = "main.md"
    outputFile = "qiita.md"

    convertMathBlocks(inputFile, outputFile)

    # Copy the output to the clipboard
    with open(outputFile, "r", encoding="utf-8") as file:
        content = file.read()
        pyperclip.copy(content)


if __name__ == "__main__":
    main()
