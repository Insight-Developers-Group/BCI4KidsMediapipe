import React, { useState, useEffect } from "react";
export default function ErrorResponsed(props) {
    const [err, setErr] = useState("e")

    function updateErr(msg) {
        setErr(msg);
    }

    useEffect(() => {
        if (props.msg === "error: invalid state exception") {
            updateErr("invalid_state_exception")
        }
        else if (props.msg === "error: no face detected") {
            updateErr("no_face_detected_exception")
        }
        else if (props.msg === "error: multiple faces detected") {
            updateErr("multi_face_detected_exception")
        }
        else if (props.msg === "error: invalid model type") {
            updateErr("invalid_model_type")
        }
        else if (props.msg === "error: df generator failed") {
            updateErr("df_generator_exception")
        }
        else if (props.msg === "error: state generator failed") {
            updateErr("state_generator_exception")
        }
        else if (props.msg === "error: answer generator failed") {
            updateErr("answer_generator_exception")
        }
        else {
            updateErr("")
        }
    }, [props.msg]);

    return (
        <div className="error-response">
            {err}
        </div>
    )
}