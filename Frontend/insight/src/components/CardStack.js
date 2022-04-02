import Card from "./Card";
import React, { useEffect } from "react";
// Component function for the bottom-right card stack item
function CardStack(props) {
    // State of firstCard and secondCard affects the type of each card (yes/no)
    // Valid states are: "card_yes", "card_no", and "card_none"
    const [firstCardFaded, setFirstCardFaded] = React.useState(false);
    let cardStackClass = "card_stack";
    if (props.flipCardsMode) cardStackClass += " cards-flipped";

    function addYesCard() {
        if (props.firstCard !== "card_waiting") {
            props.setSecondCard(props.firstCard);
            props.setFirstCard("card_yes");
        } else {
            props.setFirstCard("card_yes");
        }
    }

    function addNoCard() {
        if (props.firstCard !== "card_waiting") {
            props.setSecondCard(props.firstCard);
            props.setFirstCard("card_no");
        } else {
            props.setFirstCard("card_no");
        }
    }

    function addWaitingCard() {
        if (
            props.firstCard !== "card_waiting" &&
            props.firstCard !== "card_none"
        ) {
            props.setSecondCard(props.firstCard);
            props.setFirstCard("card_waiting");
        }
    }

    const FADE_DELAY = 5000; // Time before first card fades out
    const WAITING_DELAY = 5000; // Time before first card replaced with waiting card (this delay happens after FADE_DELAY)

    useEffect(() => {
        setFirstCardFaded(false);

        if (props.response === "yes") {
            addYesCard();
            props.setResponse(""); // Need to clear this so subsequent identical responses are handled correctly
        } else if (props.response === "no") {
            addNoCard();
            props.setResponse("");
        } else if (props.response === "wait") {
            addWaitingCard();
            props.setResponse("");
        }

        // Fade out cards after a specified number of seconds
        // Shows users that there hasn't been a response for a while
        let timer2;
        const timer = setTimeout(() => {
            if (props.firstCard !== "card_waiting") setFirstCardFaded(true);
            timer2 = setTimeout(() => {
                setFirstCardFaded(false);
                addWaitingCard();
            }, WAITING_DELAY);
        }, FADE_DELAY);

        return () => {
            clearTimeout(timer);
            clearTimeout(timer2);
        };

        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [props.response]);

    return (
        <div className={cardStackClass} data-testid="card_stack">
            <Card
                order="card_first"
                cardClass={props.firstCard}
                testid="first_card"
                faded={firstCardFaded}
                colorBlindMode={props.colorBlindMode}
                darkTextMode={props.darkTextMode}
            />
            <Card
                order="card_second"
                cardClass={props.secondCard}
                testid="second_card"
                faded={false}
                colorBlindMode={props.colorBlindMode}
                darkTextMode={props.darkTextMode}
            />
        </div>
    );
}

export default CardStack;
