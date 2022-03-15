import Card from "./Card";
import React, { useEffect } from "react";
// Component function for the bottom-right card stack item
function CardStack(props) {
    // State of firstCard and secondCard affects the type of each card (yes/no)
    // Valid states are: "card_yes", "card_no", and "card_none"
    function addYesCard() {
        props.setSecondCard(props.firstCard);
        props.setFirstCard("card_yes");
    }

    function addNoCard() {
        props.setSecondCard(props.firstCard);
        props.setFirstCard("card_no");
    }

    useEffect(() => {
        if (props.response === "yes") {
            addYesCard();
            props.setResponse(""); // Need to clear this so subsequent identical responses are handled correctly
        } else if (props.response === "no") {
            addNoCard();
            props.setResponse("");
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [props.response]);

    return (
        <div className="card_stack" data-testid="card_stack">
            <Card
                order="card_first"
                cardClass={props.firstCard}
                data-testid="first_card"
            />
            <Card
                order="card_second"
                cardClass={props.secondCard}
                data-testid="second_card"
            />
        </div>
    );
}

export default CardStack;
