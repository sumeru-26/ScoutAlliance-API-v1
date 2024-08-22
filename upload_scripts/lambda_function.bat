echo off
setlocal

set /P "uploadInput=File to be uploaded: "
set /P "lambdaFunction=Name of Lambda function: "
set uploadInput=%uploadInput:/=\%
set uploadFile=..\%uploadInput%

echo "Copying %uploadInput%..."
echo off

xcopy %uploadFile% .

echo "Generating .zip file..."

for /f "delims=" %%i in ("%uploadInput%") do set "fileName=%%~nxi"

tar.exe -a -cf aws_lambda_artifact.zip %fileName%

del %fileName%

echo "Uploading to AWS Lambda..."

aws lambda update-function-code --function-name %lambdaFunction% --zip-file "fileb://aws_lambda_artifact.zip"

del aws_lambda_artifact.zip

endlocal