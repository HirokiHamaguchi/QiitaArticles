import pyperclip


def convertMathBlocks(inputFile, outputFile):
    try:
        with open(inputFile, "r", encoding="utf-8") as file:
            content = file.read()

        lines = content.splitlines()[2:]

        convertedLines = []
        mathBlockOpen = False

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
            else:
                convertedLines.append(line)

        convertedContent = "\n".join(convertedLines) + "\n"

        convertedContent = convertedContent.replace("\n\n\n", "\n\n")
        convertedContent = convertedContent.replace("\n\n\n", "\n\n")
        convertedContent = convertedContent.replace("\n\n\n", "\n\n")

        with open(outputFile, "w", encoding="utf-8") as file:
            file.write(convertedContent)

        print(f"Conversion completed successfully. Output saved to {outputFile}")

    except FileNotFoundError:
        print(f"Error: The file {inputFile} does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


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
