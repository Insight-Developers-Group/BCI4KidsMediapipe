// Copyright 2019 The MediaPipe Authors.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// An example of sending OpenCV webcam frames into a MediaPipe graph.
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <chrono>
#include <ctime>    
#include <time.h>

#include "absl/flags/flag.h"
#include "absl/flags/parse.h"
#include "mediapipe/framework/calculator_framework.h"
#include "mediapipe/framework/formats/image_frame.h"
#include "mediapipe/framework/formats/image_frame_opencv.h"
#include "mediapipe/framework/port/file_helpers.h"
#include "mediapipe/framework/port/opencv_highgui_inc.h"
#include "mediapipe/framework/port/opencv_imgproc_inc.h"
#include "mediapipe/framework/port/opencv_video_inc.h"
#include "mediapipe/framework/port/parse_text_proto.h"
#include "mediapipe/framework/port/status.h"
//---------------------
//Take stream from /mediapipe/graphs/hand_tracking/hand_detection_desktop_live.pbtxt
// RendererSubgraph - LANDMARKS:hand_landmarks
#include "mediapipe/calculators/util/landmarks_to_render_data_calculator.pb.h"
#include "mediapipe/framework/formats/landmark.pb.h"
//-------------------------
constexpr char kInputStream[] = "input_video";
constexpr char kOutputStream[] = "output_video";
constexpr char kLandmarksStream[] = "multi_face_landmarks";
constexpr char kOutputFaceCountStream[] = "face_count";
constexpr char kWindowName[] = "MediaPipe";

const int kNumberOfFacialLandmarks = 468;

ABSL_FLAG(std::string, calculator_graph_config_file, "",
          "Name of file containing text format CalculatorGraphConfig proto.");
ABSL_FLAG(std::string, input_video_path, "",
          "Full path of video to load. "
          "If not provided, attempt to use a webcam.");
ABSL_FLAG(std::string, output_video_path, "",
          "Full path of where to save result (.mp4 only). "
          "If not provided, show result in a window.");

absl::Status RunMPPGraph() {

    std::string calculator_graph_config_contents;
    MP_RETURN_IF_ERROR(mediapipe::file::GetContents(
        absl::GetFlag(FLAGS_calculator_graph_config_file),
        &calculator_graph_config_contents));
    LOG(INFO) << "Get calculator graph config contents: "
        << calculator_graph_config_contents;
    mediapipe::CalculatorGraphConfig config =
        mediapipe::ParseTextProtoOrDie<mediapipe::CalculatorGraphConfig>(
            calculator_graph_config_contents);

    LOG(INFO) << "Initialize the calculator graph.";
    mediapipe::CalculatorGraph graph;
    MP_RETURN_IF_ERROR(graph.Initialize(config));

    LOG(INFO) << "Initialize the camera or load the video.";
    cv::VideoCapture capture;
    const bool load_video = !absl::GetFlag(FLAGS_input_video_path).empty();
    if (load_video) {
        capture.open(absl::GetFlag(FLAGS_input_video_path));
    }
    else {
        capture.open(0);
    }
    RET_CHECK(capture.isOpened());

    cv::VideoWriter writer;
    const bool save_video = !absl::GetFlag(FLAGS_output_video_path).empty();
    if (!save_video) {
        cv::namedWindow(kWindowName, /*flags=WINDOW_AUTOSIZE*/ 1);
#if (CV_MAJOR_VERSION >= 3) && (CV_MINOR_VERSION >= 2)
        capture.set(cv::CAP_PROP_FRAME_WIDTH, 640);
        capture.set(cv::CAP_PROP_FRAME_HEIGHT, 480);
        capture.set(cv::CAP_PROP_FPS, 30);
#endif
    }

    LOG(INFO) << "Start running the calculator graph.";
    ASSIGN_OR_RETURN(mediapipe::OutputStreamPoller poller,
        graph.AddOutputStreamPoller(kOutputStream));

    // Check for landmarks stream
    ASSIGN_OR_RETURN(mediapipe::OutputStreamPoller face_count_poller,
        graph.AddOutputStreamPoller(kOutputFaceCountStream));

    // Face landmarks stream
    ASSIGN_OR_RETURN(mediapipe::OutputStreamPoller poller_landmark,
        graph.AddOutputStreamPoller(kLandmarksStream));

    MP_RETURN_IF_ERROR(graph.StartRun({}));


    // Create csv file for logging face landmarks
    std::time_t rawtime;
    struct tm* ptm;

    time(&rawtime);

    ptm = gmtime(&rawtime);

    std::string hour_s = std::to_string((ptm->tm_hour) % 24);
    std::string minute_s = std::to_string(ptm->tm_min);
    std::string month_s = std::to_string(ptm->tm_mon);
    std::string day_s = std::to_string(ptm->tm_mday);
    std::string log_file_name = ".\\logs\\" + month_s + "-" + day_s + "-" + hour_s + minute_s + ".csv";

  std::ofstream landmark_log_file;
  landmark_log_file.open(log_file_name);

  std::string init_log_file = "";

  for (int i = 1; i <= kNumberOfFacialLandmarks; i++)
  {
      std::string index = std::to_string(i);
      init_log_file += "x" + index + ",y" + index + ",z" + index + ",";
  }

  init_log_file += "\n";
  landmark_log_file << init_log_file;

  LOG(INFO) << "Start grabbing and processing frames.";
  bool grab_frames = true;
  while (grab_frames) {

    // Capture opencv camera or video frame.
    cv::Mat camera_frame_raw;
    capture >> camera_frame_raw;
    if (camera_frame_raw.empty()) {
      if (!load_video) {
        LOG(INFO) << "Ignore empty frames from camera.";
        continue;
      }
      LOG(INFO) << "Empty frame, end of video reached.";
      break;
    }
    cv::Mat camera_frame;
    cv::cvtColor(camera_frame_raw, camera_frame, cv::COLOR_BGR2RGB);
    if (!load_video) {
      cv::flip(camera_frame, camera_frame, /*flipcode=HORIZONTAL*/ 1);
    }

    // Wrap Mat into an ImageFrame.
    auto input_frame = absl::make_unique<mediapipe::ImageFrame>(
        mediapipe::ImageFormat::SRGB, camera_frame.cols, camera_frame.rows,
        mediapipe::ImageFrame::kDefaultAlignmentBoundary);
    cv::Mat input_frame_mat = mediapipe::formats::MatView(input_frame.get());
    camera_frame.copyTo(input_frame_mat);

    // Send image packet into the graph.
    size_t frame_timestamp_us =
        (double)cv::getTickCount() / (double)cv::getTickFrequency() * 1e6;
    MP_RETURN_IF_ERROR(graph.AddPacketToInputStream(
        kInputStream, mediapipe::Adopt(input_frame.release())
                          .At(mediapipe::Timestamp(frame_timestamp_us))));

    // Get the graph result packet, or stop if that fails.
    mediapipe::Packet packet;
    mediapipe::Packet face_count_packet;
    mediapipe::Packet landmark_packet;

    // Polling the poller to get landmark packet
    if (!poller.Next(&packet)) break;
    if (!face_count_poller.Next(&face_count_packet)) break;

    auto& face_count = face_count_packet.Get<int>();

    if (face_count >= 1 && poller_landmark.Next(&landmark_packet))
    {
        // Use packet.Get to recover values from packet
        auto & output_landmarks = landmark_packet.Get<std::vector<::mediapipe::NormalizedLandmarkList>>();

        // Log landmark values in csv *landmark_list.DebugString()
        if (output_landmarks.size() > 1)
        {
            LOG(INFO) << "ERROR_MULTIPLE_FACES_DETECTED";
        }
        else if (output_landmarks.size() == 1)
        {
            std::string landmark_log_frame = "";

            const ::mediapipe::NormalizedLandmarkList& landmark_list = output_landmarks[0];
            for (int i = 0; i < kNumberOfFacialLandmarks; i++)
            {
                landmark_log_frame +=
                    std::to_string(landmark_list.landmark(i).x()) + "," +
                    std::to_string(landmark_list.landmark(i).y()) + "," +
                    std::to_string(landmark_list.landmark(i).z()) + ",";
            }
            landmark_log_frame += "\n";
            landmark_log_file << landmark_log_frame;
        }
    }
    else
    {
        LOG(INFO) << "ERROR_NO_FACE_DETECTED";
    }

    // Use packet.Get to recover values from packet
    auto& output_frame = packet.Get<mediapipe::ImageFrame>();

    // Convert back to opencv for display or saving.
    cv::Mat output_frame_mat = mediapipe::formats::MatView(&output_frame);
    cv::cvtColor(output_frame_mat, output_frame_mat, cv::COLOR_RGB2BGR);
    if (save_video) {
      if (!writer.isOpened()) {
        LOG(INFO) << "Prepare video writer.";
        writer.open(absl::GetFlag(FLAGS_output_video_path),
                    mediapipe::fourcc('a', 'v', 'c', '1'),  // .mp4
                    capture.get(cv::CAP_PROP_FPS), output_frame_mat.size());
        RET_CHECK(writer.isOpened());
      }
      writer.write(output_frame_mat);
    } else {
      cv::imshow(kWindowName, output_frame_mat);
      // Press any key to exit.
      const int pressed_key = cv::waitKey(5);
      if (pressed_key >= 0 && pressed_key != 255) grab_frames = false;
    }
  }

  LOG(INFO) << "Shutting down.";
  
  landmark_log_file.close();
  if (writer.isOpened()) writer.release();
  MP_RETURN_IF_ERROR(graph.CloseInputStream(kInputStream));
  return graph.WaitUntilDone();
}

int main(int argc, char** argv) {
  google::InitGoogleLogging(argv[0]);
  absl::ParseCommandLine(argc, argv);
  absl::Status run_status = RunMPPGraph();
  if (!run_status.ok()) {
    LOG(ERROR) << "Failed to run the graph: " << run_status.message();
    return EXIT_FAILURE;
  } else {
    LOG(INFO) << "Success!";
  }
  return EXIT_SUCCESS;
}