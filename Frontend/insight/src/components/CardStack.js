import Card from './Card'
import React, { Component, useEffect, useState } from 'react'
// Component function for the bottom-right card stack item
function CardStack(props) {

    // State of firstCard and secondCard affects the type of each card (yes/no)
    // Valid states are: "card_yes", "card_no", and "card_none"
    let [firstCard, setFirstCard] = useState("card_yes")
    let [secondCard, setSecondCard] = useState("card_no")
    let [prevResponse, setPrevResponse] = useState(props.response)

    function addYesCard() {
        setSecondCard(firstCard)
        setFirstCard("card_yes")
    }

    function addNoCard() {
        setSecondCard(firstCard)
        setFirstCard("card_no")
    }

    useEffect(() => {
        if (props.response === 'yes') {
            addYesCard();
            setPrevResponse(props.response);
        }
        else if (props.response === 'no') {
            addNoCard();
            setPrevResponse(props.response);
        }
        // else if (props.response === prevResponse) {
        //     if (props.response === 'yes') {
        //         addYesCard();
        //         setPrevResponse(props.response);
        //     }
        //     else if (props.response === 'no') {
        //         addNoCard();
        //         setPrevResponse(props.response);
        //     }
        // }

    }, [props.response]);

    return (
        <div className="card_stack" data-testid='card_stack'>
            <Card order="card_first" cardClass={firstCard} />
            <Card order="card_second" cardClass={secondCard} />;
        </div>
    )
}

export default CardStack
