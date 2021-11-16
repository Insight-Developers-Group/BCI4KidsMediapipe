// Copyright 2020 The MediaPipe Authors.
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

#ifndef MEDIAPIPE_CALCULATORS_UTIL_COUNTING_VECTOR_SIZE_CALCULATOR_H
#define MEDIAPIPE_CALCULATORS_UTIL_COUNTING_VECTOR_SIZE_CALCULATOR_H

#include "mediapipe/framework/calculator_framework.h"
#include "mediapipe/framework/formats/landmark.pb.h"

namespace mediapipe {

    // A calculator that count input landmarksList size.
    //
    // Count input landmark(std::vector<NormalizedLandmarkList>) and return this 
    // value to ouput_stream. Input IMAGE has no effect on calculation, but is used to
    // ensure that the calculator works even when the landmark is empty. And if the 
    // input landmark is empty, the number of faces found is zero.
    //
    // Example config:
    // node {
    //   calculator: "CountingVectorSizeCalculator"
    //   input_stream: "IMAGE:input_image"
    //   input_stream: "LANDMARKS:multi_face_landmarks"
    //   output_stream: "COUNT:face_count"
    // }

    template <typename VectorT>
    class CountingVectorSizeCalculator : public CalculatorBase {
    public:
        static ::mediapipe::Status GetContract(CalculatorContract* cc) {
            // Check tag.
            RET_CHECK(cc->Inputs().HasTag("CLOCK"));
            cc->Inputs().Tag("CLOCK").SetAny();
            RET_CHECK(cc->Inputs().HasTag("VECTOR"));
            cc->Inputs().Tag("VECTOR").Set<VectorT>();
            RET_CHECK(cc->Outputs().HasTag("COUNT"));
            cc->Outputs().Tag("COUNT").Set<int>();

            return ::mediapipe::OkStatus();
        }

        ::mediapipe::Status Process(CalculatorContext* cc) {
            std::unique_ptr<int> face_count;
            if (!cc->Inputs().Tag("VECTOR").IsEmpty()) {
                const auto& landmarks = cc->Inputs().Tag("VECTOR").Get<VectorT>();
                face_count = absl::make_unique<int>(landmarks.size());
            }
            else {
                face_count = absl::make_unique<int>(0);
            }
            cc->Outputs().Tag("COUNT").Add(face_count.release(), cc->InputTimestamp());

            return ::mediapipe::OkStatus();
        };
    };

}

#endif  // MEDIAPIPE_CALCULATORS_UTIL_COUNTING_VECTOR_SIZE_CALCULATOR_H