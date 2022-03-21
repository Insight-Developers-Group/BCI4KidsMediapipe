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
                errCmp.current.innerHTML = "Oops! We couldn't validate that state";
            }
            else if (props.msg === "error: no face detected") {
                errCmp.current.innerHTML = "Oops! We can't see you"
            }
            else if (props.msg === "error: multiple faces detected") {
                errCmp.current.innerHTML = "Oops! too many people in the frame"
            }
            else if (props.msg === "error: invalid model type") {
                errCmp.current.innerHTML = "Oops! we couldn't validate that model"
            }
            else if (props.msg === "error: df generator failed") {
                errCmp.current.innerHTML = "Oops! DF generator failed"
            }
            else if (props.msg === "error: state generator failed") {
                errCmp.current.innerHTML = "Oops! State generator failed"
            }
            else if (props.msg === "error: answer generator failed") {
                errCmp.current.innerHTML = "Oops! We couldn't generate an answer"
            }
        }
    }, [props.msg]);

    return (
        <div className="error-response" ref={errCmp}>
        </div>
    )
}