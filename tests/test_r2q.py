from R2Q import process_lines


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
