import React, { useState, useEffect, useRef } from "react";
export default function ErrorResponse(props) {
    const errCmp = useRef();

    useEffect(() => {

        if (props.msg === '') {
            errCmp.current.style.display = 'none';
        }

        else if (props.msg === "error: invalid state exception") {
            errCmp.current.style.display = 'block';
            errCmp.current.innerHTML = 'invalid_state_exception';
        }
        else if (props.msg === "error: no face detected") {
            errCmp.current.style.display = 'block';
            errCmp.current.innerHTML = 'no_face_detected_exception'
        }
        else if (props.msg === "error: multiple faces detected") {
            errCmp.current.style.display = 'block';
            errCmp.current.innerHTML = 'multi_face_detected_exception'
        }
        else if (props.msg === "error: invalid model type") {
            errCmp.current.style.display = 'block';
            errCmp.current.innerHTML = 'invalid_model_type'
        }
        else if (props.msg === "error: df generator failed") {
            errCmp.current.style.display = 'block';
            errCmp.current.innerHTML = 'df_generator_exception'
        }
        else if (props.msg === "error: state generator failed") {
            errCmp.current.style.display = 'block';
            errCmp.current.innerHTML = 'state_generator_exception'
        }
        else if (props.msg === "error: answer generator failed") {
            errCmp.current.style.display = 'block';
            errCmp.current.innerHTML = 'answer_generator_exception'
        }
    }, [props.msg]);

    return (
        <div className="error-response" ref={errCmp}>
        </div>
    )
}