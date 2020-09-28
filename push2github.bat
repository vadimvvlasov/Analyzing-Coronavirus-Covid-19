jupyter nbconvert --execute --to html --inplace --allow-errors --ExecutePreprocessor.timeout=-1 CovID.ipynb
git status
git add .
git status
git commit -m "daily commit"
git status
git push origin
git status