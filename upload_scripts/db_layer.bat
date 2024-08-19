echo off
setlocal

echo "Generating dependencies..."

pip install -t dependencies_temp -r ../requirements.txt

mkdir python
cd python
mkdir lib
cd lib
mkdir python3.12
cd python3.12
mkdir site-packages

cd../../..

echo "Copying files..."

xcopy /s dependencies_temp python\lib\python3.12\site-packages
xcopy ..\db.py python

echo "Generating .zip file..."

tar.exe -a -cf lambda_db_layer.zip python

@REM echo "Current Versions:"
@REM aws lambda list-layer-versions --layer-name v1_ScoutAlliance_db_layer

@REM set /P "version=New layer version: "
set /P "description=Description: "

aws lambda publish-layer-version --layer-name v1_ScoutAlliance_db_layer --description "%description%" --zip-file "fileb://lambda_db_layer.zip" --compatible-runtimes python3.12 --compatible-architectures x86_64

pause

rd /s dependencies_temp
rd /s python
del lambda_db_layer.zip

endlocal