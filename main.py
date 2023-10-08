import pylab
from Foundation import NSData
from AppKit import NSPasteboard, NSPasteboardTypeString, NSPasteboardTypePNG, NSPasteboardTypeTIFF


def get_formula_from_input() -> str:
    return f"${input('formula:')}$"

def save_formula_as_image(formula: str, file_path: str) -> str:
    """
    https://stackoverflow.com/a/14163131
    """
    fig = pylab.figure()
    text = fig.text(0, 0, formula)

    # Saving the figure will render the text.
    dpi = 300
    fig.savefig(file_path, dpi=dpi)

    # Now we can work with text's bounding box.
    bbox = text.get_window_extent()
    width, height = bbox.size / float(dpi) + 0.005
    # Adjust the figure size so it can hold the entire text.
    fig.set_size_inches((width, height))

    # Adjust text's vertical position.
    dy = (bbox.ymin/float(dpi))/height
    text.set_position((0, -dy))

    # Save the adjusted text.
    fig.savefig(file_path, dpi=dpi)

    return file_path

def copy_image_to_clipboard(file_path: str) -> bool:
  """
  https://stackoverflow.com/a/76159627
  """
  filename = "formula.png"  # set this to filepath where img is saved
  pasteboard = NSPasteboard.generalPasteboard()
  image_data = NSData.dataWithContentsOfFile_(filename)
  pasteboard.clearContents()
  return pasteboard.setData_forType_(image_data, NSPasteboardTypePNG)

def get_text_from_clipboard() -> str:
    """
    https://stackoverflow.com/a/8317794 (Updated for python3)
    """
    pasteboard = NSPasteboard.generalPasteboard()
    text = pasteboard.stringForType_(NSPasteboardTypeString)
    return text.strip()

def get_formula_from_clipboard() -> str:
    text = get_text_from_clipboard()
    return f"${text}$"

def main() -> None:
    # formula = get_formula_from_input() # from user input
    formula = get_formula_from_clipboard() # from clipboard
    save_formula_as_image(formula, "formula.png")
    copy_image_to_clipboard("formula.png")

if __name__ == "__main__":
   main()
