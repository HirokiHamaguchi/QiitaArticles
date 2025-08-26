def test_trick_blocks():
    blocks = []
    with open("README.md", encoding="utf-8") as f:
        lines = f.readlines()

    # <!-- trick -->の行とその下の3行を取得
    for i, line in enumerate(lines):
        if "<!-- trick -->" in line:
            assert line.strip() == "<!-- trick -->"
            assert i + 3 < len(lines)
            block = lines[i + 1 : i + 4]
            print(block)
            blocks.append(block)

    assert len(blocks) >= 2
    first_block = blocks[0]
    for idx, block in enumerate(blocks[1:], start=1):
        assert block == first_block, f"Block {idx} does not match the first block"

    print("All trick blocks are identical.")


if __name__ == "__main__":
    test_trick_blocks()
