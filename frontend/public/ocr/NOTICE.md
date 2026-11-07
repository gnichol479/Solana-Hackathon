# OCR assets

These assets are distributed to let Tesseract.js process screenshots in the browser without sending image bytes to an OCR provider.

- `worker.min.js`: Tesseract.js 7.0.0, Apache License 2.0, https://github.com/naptha/tesseract.js
- `core/*`: tesseract.js-core as installed through the locked dependency tree, Apache License 2.0, https://github.com/naptha/tesseract.js-core
- `lang/eng.traineddata.gz`: English Tesseract language data from https://tessdata.projectnaptha.com/4.0.0/eng.traineddata.gz ; Tesseract language-data project, Apache License 2.0, https://github.com/tesseract-ocr/tessdata

Upstream copyright/license text is retained in the accompanying license files. See `package-lock.json` for exact runtime versions.
