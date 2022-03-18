import React, { useState, useEffect, useRef } from "react";
export default function ErrorResponsed(props) {

    const errCmp = useRef();

    useEffect(() => {

        if (props.msg === '') {
            errCmp.current.style.display = 'none';
        }
        else {
            errCmp.current.style.display = 'block';
            if (props.msg === "error: invalid state exception") {
                errCmp.current.innerHTML = 'invalid_state_exception';
            }
            else if (props.msg === "error: no face detected") {
                errCmp.current.innerHTML = 'no_face_detected_exception'
            }
            else if (props.msg === "error: multiple faces detected") {
                errCmp.current.innerHTML = 'multi_face_detected_exception'
            }
            else if (props.msg === "error: invalid model type") {
                errCmp.current.innerHTML = 'invalid_model_type'
            }
            else if (props.msg === "error: df generator failed") {
                errCmp.current.innerHTML = 'df_generator_exception'
            }
            else if (props.msg === "error: state generator failed") {
                errCmp.current.innerHTML = 'state_generator_exception'
            }
            else if (props.msg === "error: answer generator failed") {
                errCmp.current.innerHTML = 'answer_generator_exception'
            }
        }
    }, [props.msg]);

    return (
        <div className="error-response" ref={errCmp}>
        </div>
    )
}