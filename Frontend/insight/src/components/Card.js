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
            cardLabel = "...";
            break;

        default:
            cardLabel = "";
            break;
    }
    if (props.faded) {
        return (
            <div
                className={
                    "card " +
                    props.cardClass +
                    " " +
                    props.order +
                    " card-faded"
                }
                data-testid={props.testid}>
                <h3 className="card_label" data-testid="card_label">
                    {cardLabel}
                </h3>
            </div>
        );
    }

    return (
        <div
            className={"card " + props.cardClass + " " + props.order}
            data-testid={props.testid}>
            <h3 className="card_label" data-testid="card_label">
                {cardLabel}
            </h3>
        </div>
    );
}

export default Card;
