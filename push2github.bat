jupyter nbconvert --execute --to notebook --inplace --allow-errors --ExecutePreprocessor.timeout=-1 CovID.ipynb
git status
git add .
git status
git commit -m "daily commit"
git status
git push origin
git status