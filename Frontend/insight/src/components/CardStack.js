import Card from "./Card";
import React, { Component, useEffect, useState } from "react";
// Component function for the bottom-right card stack item
function CardStack(props) {
    // State of firstCard and secondCard affects the type of each card (yes/no)
    // Valid states are: "card_yes", "card_no", and "card_none"
    let [firstCard, setFirstCard] = useState("card_yes");
    let [secondCard, setSecondCard] = useState("card_no");
    let [prevResponse, setPrevResponse] = useState(props.response);

    function addYesCard() {
        setSecondCard(firstCard);
        setFirstCard("card_yes");
    }

    function addNoCard() {
        setSecondCard(firstCard);
        setFirstCard("card_no");
    }

    useEffect(() => {
        if (props.response === "yes") {
            addYesCard();
            setPrevResponse(props.response);
        } else if (props.response === "no") {
            addNoCard();
            setPrevResponse(props.response);
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
        <div className="card_stack" data-testid="card_stack">
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
