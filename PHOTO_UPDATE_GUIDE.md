# Photo update guide

The gallery is listed by hand in `photo/index.html`. New originals go into `unprocess`, then `photo_process.py` compresses them into the live folders.

## Add new photos

1. Drop originals here (do not put them straight into the live folders):
   - Digital: `assets/img/photo/unprocess/digital/`
   - Film: `assets/img/photo/unprocess/film/`
2. From `webpage/ManlingYANG123`, run:

   ```bash
   python3 photo_process.py
   ```

   The script:
   - keeps the originals in `unprocess/{digital,film}/backup/`
   - writes compressed JPEGs (max 1920×1080, quality 85) to `assets/img/photo/digital/` or `film/`
   - replaces spaces in filenames with `_`
   - removes the files from `unprocess` after a successful compress
3. Add one tile per new file in `photo/index.html`.
   - Digital: inside `#digital-photos`
   - Film: inside `#film-photos`

```html
<button type="button" class="photo-tile" data-src="../assets/img/photo/digital/YOUR_FILE.jpg" aria-label="Open Digital photo">
  <img src="../assets/img/photo/digital/YOUR_FILE.jpg" alt="Digital photo" loading="lazy">
</button>
```

4. Commit the live compressed files and the HTML change. Do not commit `unprocess/**/backup` (full-size originals).

## Notes

- Prefer filenames with letters, numbers, `_`, and `.` only.
- `_data/photo.yml` and `_data/film.yml` are no longer used.
- After adding many photos, the scattered layout still works; no extra delay config is required.
