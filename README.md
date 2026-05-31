# Raspberry Audiobook

NFC-driven audiobook player for a Raspberry Pi. The current app can use a mock
NFC reader from the terminal while still using the real audio player and rotary
encoders on the Pi.

## Run

Install the package in your virtual environment:

```powershell
pip install -e .
```

Run with mock NFC input and the default GPIO rotary encoders:

```powershell
audiobook-player --mock
```

Run without GPIO controls for development on a non-Pi machine:

```powershell
audiobook-player --mock --no-controls
```

Default rotary encoder pins:

| Control | GPIO A | GPIO B | Behavior |
| --- | ---: | ---: | --- |
| Volume | 16 | 20 | Changes VLC player volume by 5 percent |
| Seek | 19 | 26 | Seeks 10 seconds forward or backward |

You can override them:

```powershell
audiobook-player --mock --volume-pins 16 20 --seek-pins 19 26
```

Book mappings live in `config/books.yaml`. Each NFC UID maps to a title and a
folder containing MP3 files. Files are played in sorted filename order.

## Next Hardware Features

- NFC tag scan selects the matching audiobook.
- Bookmark storage remembers UID, chapter index, and position in the current
  file.
- Buttons call the existing player methods for play/pause, next chapter, and
  previous chapter.
