# Before making the repository public

Copy this folder into a **new** repository rather than publishing the private working repository, so that nothing from its history becomes public.

## 1. Placeholders

* `LICENSE`: copyright holder (authors or university).
* `CITATION.cff`: authors, ORCID, repository URL, release date.
* `README.md`: author list and URL in the BibTeX block.

## 2. Checks

```bash
pip install -r requirements.txt && pip install -e .
pytest

# no notebook outputs or embedded images
grep -l '"output_type"' notebooks/*.ipynb || echo "no outputs"

# no secrets
gitleaks detect --source . --no-git -v

# no data or weights besides the allowed exceptions
find . -path ./.git -prune -o -type f \( -iname "*.jpg" -o -iname "*.png" -o -iname "*.npy" -o -iname "*.npz" \
  -o -iname "*.pt" -o -iname "*.onnx" -o -iname "*.zip" \) -print | grep -v -e "^./docs/figures/" -e "^./examples/"
```

If a Kaggle key or server key was ever committed to the private repository, regenerate it, even though it is not copied here.

## 3. Publish

1. Push, then set the repository to public.
2. On zenodo.org, sign in with GitHub and enable archiving for this repository.
3. Create release `v1.0.0` matching the manuscript submitted to the journal. Zenodo issues a DOI.
4. Add the DOI to the paper's Data Availability Statement, `CITATION.cff` and the README.
