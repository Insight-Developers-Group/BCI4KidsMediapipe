import React from "react";

// Component function for the individual cards in the card stack component (at "./CardStack.js")
function Card(props) {
    let cardLabel;
    switch (props.cardClass) {
        case "card_yes":
            cardLabel = "Yes";
            break;

        case "card_no":
            cardLabel = "No";
            break;

        case "card_waiting":
            return (
                <div
                    className={"card " + props.cardClass + " " + props.order}
                    data-testid={props.testid}>
                    <span className="waiting-dots-cont">
                        {" "}
                        <span className="waiting-dot dot-1"></span>{" "}
                        <span className="waiting-dot dot-2"></span>{" "}
                        <span className="waiting-dot dot-3"></span>{" "}
                    </span>
                </div>
            );

        default:
            cardLabel = "";
            break;
    }

    return (
        <div className={"card " + props.cardClass + " " + props.order}>
            <h3 className="card_label">{cardLabel}</h3>
        </div>
    );
}

export default Card;
