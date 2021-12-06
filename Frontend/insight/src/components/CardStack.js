import React from 'react'
import PropTypes from 'prop-types'
import Card from './Card'

// Component function for the bottom-right card stack item
function CardStack(props) {

    // State of firstCard and secondCard affects the type of each card (yes/no)
    // Valid states are: "card_yes", "card_no", and "card_none"
    let [firstCard, setFirstCard] = React.useState("card_yes")
    let [secondCard, setSecondCard] = React.useState("card_no")

    function addYesCard() {
        setSecondCard(firstCard)
        setFirstCard("yes")
    }

    function addNoCard() {
        setSecondCard(firstCard)
        setSecondCard("no")
    }

    return (
        <div id="card_stack">
            <Card order="card_first" cardClass={firstCard}/>
            <Card order="card_second" cardClass={secondCard}/>
        </div>
    )
}

CardStack.propTypes = {

}

export default CardStack
