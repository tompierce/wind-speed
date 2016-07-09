rm -rf package.zip
zip -9 package.zip *.py
zip -r9 package.zip wind/*.py
saved_dir=`pwd`
cd venv/lib/python2.7/site-packages/
zip -r9 $saved_dir/package.zip *