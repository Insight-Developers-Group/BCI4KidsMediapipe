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

        default:
            cardLabel = "";
            break;
    }

    return (
        <div className={"card " + props.cardClass + " " + props.order}>
            <h3 className="card_label" data-testid="card_label">
                {cardLabel}
            </h3>
        </div>
    );
}

export default Card;
