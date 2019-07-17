pyenv local Sci-Python 2.7.15

# Install iPython kernel
python -m ipykernel install --user \
  --name Naukluft --display-name "Python (Scientific)" > /dev/null

pip install -e webapp/Attitude
