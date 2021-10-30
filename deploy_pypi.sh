conda activate rnd_env
python setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*
# Input username quangduong109 and password to publish
