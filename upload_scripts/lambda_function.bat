echo off

setlocal

set /P "uploadInput=File to be uploaded: "

IF "%uploadInput%"=="" set /p uploadInput=<lambda_function_cache.txt
IF NOT "%uploadInput%"=="" (echo %uploadInput%)>lambda_function_cache.txt

setlocal

set lambdaFunction=%uploadInput:/=_%
set lambdaFunction=v1_ScoutAlliance_%lambdaFunction:~0,-3%
set uploadFile=..\%uploadInput:/=\%

echo lambda function: %lambdaFunction%

echo Copying %uploadInput%...

xcopy %uploadFile% .

echo Generating .zip file...

for /f "delims=" %%i in ("%uploadInput%") do set "fileName=%%~nxi"

tar.exe -a -cf aws_lambda_artifact.zip %fileName%

del %fileName%

echo Uploading to AWS Lambda...

aws lambda update-function-code --function-name %lambdaFunction% --zip-file "fileb://aws_lambda_artifact.zip"

del aws_lambda_artifact.zip

endlocal