import React, { useState, useEffect } from "react";

// Component for showing error responses from the server to the user
export default function ErrorResponse(props) {
    const [errorLabel, setErrorLabel] = useState("");

    useEffect(() => {
        switch (props.msg) {
            case "error: invalid state exception":
                setErrorLabel("Oops! We couldn't validate that state");
                break;
            case "error: no face detected":
                setErrorLabel("Oops! We can't see you");
                break;
            case "error: multiple faces detected":
                setErrorLabel("Oops! too many people in the frame");
                break;
            case "error: invalid model type":
                setErrorLabel("Oops! we couldn't validate that model");
                break;
            case "error: df generator failed":
                setErrorLabel("Oops! DF generator failed");
                break;
            case "error: state generator failed":
                setErrorLabel("Oops! State generator failed");
                break;
            case "error: answer generator failed":
                setErrorLabel("Oops! We couldn't generate an answer");
                break;
            default:
                setErrorLabel("");
                break;
        }
    }, [props.msg]);

    return (
        <>
            {errorLabel !== "" && (
                <div className="error-holder">
                    <p className="error-response">{errorLabel}</p>
                </div>
            )}
        </>
    );
}
