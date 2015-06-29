# Simple RSS Feed Reader

This is a simple Python web server, which can run either as a standalone script or on Amazon Web services.


## Standalone Version

Requires Python 2.7

- Clone this repository
- Run navigate to the directory `standalone`
- Run `python application.py`
- Open a web browser, and enter `localhost:8012/application.py`
- Enter an RSS URL


### Notes on the standalone version
- This does not need a web server to be running. The program itself is a simple HTTP server.
- The server runs indefinitely, to close it, kill it manually (`Ctrl+C` in Linux).


## AWS Version

- Runs on Python 3. 
- Configured for `Python` on `Preconfigured for Docker` platform in AWS Elastic Beanstalk
- Upload and deploy the `aws` directory as a `.zip` file to application console

## Contact
- mourjo.sen@inria.fr
