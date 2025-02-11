import re
import os

links = {
    "proximalOperatorRef": "https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/e2324fbe-e50a-03dc-2b8b-5ead5494eee5.png",
    "convexConjugateWiki": "https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/1812d220-4bff-aff1-63c7-a9496d7b0e21.png",
    "infimalConvolution": "https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/0d1a53cd-7935-65d6-4088-eb6dbff882d3.png",
    "convexConjugate": "https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/a407e54b-9291-42ad-6e63-c5ca29e5cfc3.png",
    "Huber": "https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/2dc2792c-46bd-aa08-d614-463f53a90955.png",
    "softThresholding": "https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/1ffa3b33-ef13-8e51-6188-9d9b49d8e3d1.png",
    "proximalOperator": "https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/af5bd425-a6c6-aeb7-197d-0d3324a224e1.png",
    "Huber2": "https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/a6982f28-eff5-9375-b5af-53f0edc16467.png",
    "subgradient": "https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/c14e59e0-10b9-9f75-2f0f-086e7a138a82.png",
    "generalMoreauEnvelope": "https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/905155/5a562da9-b66a-81fc-91ed-e2f748e744a1.png",
}


def main():
    with open(
        os.path.join(os.path.dirname(__file__), "README.md"),
        "r",
        encoding="UTF-8",
    ) as f:
        content = f.read()

    lines = content.splitlines()
    assert lines[0].startswith("# ")
    assert lines[1].strip() == ""
    lines = lines[2:]

    res = [
        "<!-- markdownlint-disable MD041 -->",
        "",
    ]
    mathBlockOpen = False
    nextIgnore = False

    for line in lines:
        if line.strip() == "$$":
            if not mathBlockOpen:
                res.append("\n```math")
                mathBlockOpen = True
            else:
                res.append("```\n")
                mathBlockOpen = False
        elif line.strip() == "> $$":
            if not mathBlockOpen:
                res.append(">")
                res.append("> ```math")
                mathBlockOpen = True
            else:
                res.append("> ```")
                res.append(">")
                mathBlockOpen = False
        elif line.startswith("!["):
            if nextIgnore:
                res.append(line)
                nextIgnore = False
                continue
            # ![alt](url) -> <img width=100% src="url" alt="alt">
            alt = line[line.find("[") + 1 : line.find("]")]
            url = line[line.find("(") + 1 : line.find(")")]
            assert alt in links, f"{alt} is not in links"
            res.append(f'<img width=100% src="{links[alt]}" alt="{alt}">')
        elif line.strip() == "<!-- ignore -->":
            nextIgnore = True
            continue
        else:
            res.append(line)

    res = "\n".join(res) + "\n"

    res = res.replace("\n\n\n", "\n\n")
    res = res.replace("\n\n\n", "\n\n")
    res = res.replace("\n\n\n", "\n\n")

    res = res.replace("\\coloneqq", "\\mathrel{\\vcenter{:}}=")
    res = res.replace("{dcases}", "{cases}")

    if re.search(r"\\{[a-zA-Z0-9]", res):
        print("Warning: \\{[a-zA-Z0-9] found. Add space after {")
    res = res.replace("\\{", "\\lbrace")
    res = res.replace("\\}", "\\rbrace")

    if res.count("\\,"):
        print("Warning: \\, found. Use \\ instead.")

    cnt = res.count("\\|")
    if cnt % 2 == 1:
        raise ValueError(f"Odd number of \\| found: {cnt}")

    lastIdx = 0
    res2 = ""
    for vertNum, resIdx in enumerate(re.finditer(r"\\\|", res)):
        res2 += res[lastIdx : resIdx.start()]
        if vertNum % 2 == 0:
            res2 += "\\lVert"
        else:
            res2 += "\\rVert"
        lastIdx = resIdx.end()
    res2 += res[lastIdx:]
    res = res2

    with open(
        os.path.join(os.path.dirname(__file__), "Qiita.md"),
        "w",
        encoding="UTF-8",
    ) as f:
        f.write(res)


if __name__ == "__main__":
    main()
