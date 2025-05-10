## Simple Page for Blogs

#### Instruction for setup are in AM.xlsx

## Dockerization - for src_web

1.  Start DockerDesktop or other Docker

running commands from a src_web's parent folder

2.  build docker based on image: docker build -t vvl-app .
3.  test docker locally: docker run -d -p 8000:8000 vvl-app
4.  tag docker: docker tag vvl-app europe-west1-docker.pkg.dev/ai01-51d16/ai25/vvl-app:latest
5.  push to artifact registry on gcp: docker push europe-west1-docker.pkg.dev/ai01-51d16/ai25/vvl-app:latest

6.  go to artifact registry (https://console.cloud.google.com/artifacts?project=ai01-51d16&invt=Abw1EQ&inv=1) and find the deployed docker container and deploy to cloud run (delete the running service if exist)
7.  in setting up cloud run service,
    - change the location (to europe-west1 - Belgium)
    - allow unauthenticated access
    - and container port (to 8000)
