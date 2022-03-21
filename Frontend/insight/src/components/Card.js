import React from "react";

// Component function for the individual cards in the card stack component (at "./CardStack.js")
function Card(props) {
    let fullCardClass = "card " + props.cardClass + " " + props.order;

    if (props.faded) {
        fullCardClass += " card-faded";
    }

    if (props.colorBlindMode) {
        fullCardClass += " " + props.cardClass + "-colorblind";
    }

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
                <div className={fullCardClass} data-testid={props.testid}>
                    <span class="waiting-dots-cont">
                        {" "}
                        <span class="waiting-dot dot-1"></span>{" "}
                        <span class="waiting-dot dot-2"></span>{" "}
                        <span class="waiting-dot dot-3"></span>{" "}
                    </span>
                </div>
            );

        default:
            cardLabel = "";
            break;
    }

    return (
        <div className={fullCardClass} data-testid={props.testid}>
            <h3 className="card_label" data-testid="card_label">
                {cardLabel}
            </h3>
        </div>
    );
}

export default Card;
