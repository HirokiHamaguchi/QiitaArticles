from R2Q import process_lines, replace_patterns, replace_vertical_bars


def test_process_lines_handles_parentheses_in_image_alt():
    line = (
        "![Caratheodory'sTheorem(ConvexHull)_Wiki]"
        "(https://example.com/Wiki.png)"
    )

    result = process_lines([line], [], ".")

    assert (
        '<img width=100% src="https://example.com/Wiki.png" '
        'alt="Caratheodory\'sTheorem(ConvexHull)_Wiki">'
    ) in result


def test_process_lines_handles_parentheses_in_image_url_and_multiple_images():
    line = (
        "before ![first](https://example.com/image_(1).png) "
        "after ![second](https://example.com/image-2.png)"
    )

    result = process_lines([line], [], ".")

    assert 'src="https://example.com/image_(1).png" alt="first"' in result
    assert 'src="https://example.com/image-2.png" alt="second"' in result


def test_replace_patterns_separates_brace_commands_from_following_letters():
    result = replace_patterns(r"\{x_1,\ldots,x_n\}X \left\{n\right\}y")

    assert result == (
        r"\lbrace x_1,\ldots,x_n\rbrace X \left\lbrace n\right\rbrace y"
    )


def test_replace_vertical_bars_separates_commands_from_following_letters():
    result = replace_vertical_bars(r"\|X\|y + \|x_k-L\|_2")

    assert result == r"\lVert X\rVert y + \lVert x_k-L\rVert _2"
