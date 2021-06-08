## pipenv pack packages to zip (aws lambda)
```shell
mkdir output
pipenv lock -r > requirements.txt
pip install -r requirements.txt --no-deps -t output
```
[source](https://github.com/pypa/pipenv/issues/2705#issuecomment-410949164)

```shell
cp credentials.json output
cp *.py output
cd output
zip -r ../output.zip .
```