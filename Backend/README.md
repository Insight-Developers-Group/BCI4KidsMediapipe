# Insight
Insight uses lightweight iris and facial tracking to translate movements into yes/no communications

## First Time Setup

1. Follow instructions on the MediaPipe website to get set up for the use of MediaPipe** https://google.github.io/mediapipe/getting_started/install.html#installing-on-windows

** Note that step 7 and 9 are optional as our project already has the needed files from the MediaPipe github repository

2. Copy the repository WORKSPACE file located in the workplace_template folder to the main working directory as follows: 
![Alt text](msc/read_me_workspace.jpg?raw=true "Title")

3. Edit the following path in the WORKSPACE file to point to the opencv build folder

```bash
new_local_repository(
    name = "windows_opencv",
    build_file = "@//third_party:opencv_windows.BUILD",
    path = "C:\\YOUR\\PATH\\HERE\\opencv\\build",
)
```

## Building and Running the Project with Bazel

```bash 
C:\Users\Username\BCI4KidsMediapipe_repo> bazel build -c opt --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/insight/insight_mediapipe/face_mesh:face_mesh_cpu

C:\Users\Username\BCI4KidsMediapipe_repo> set GLOG_logtostderr=1

C:\Users\Username\BCI4KidsMediapipe_repo> bazel-bin\mediapipe\insight\insight_mediapipe\face_mesh\face_mesh_cpu --calculator_graph_config_file=mediapipe\graphs\face_mesh\face_mesh_desktop_live.pbtxt
```

