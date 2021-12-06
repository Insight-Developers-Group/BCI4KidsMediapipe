import React from 'react'
import PropTypes from 'prop-types'
import Card from './Card'

function CardStack(props) {

    const [firstCard, setFirstCard] = React.useState("none")
    const [secondCard, setSecondCard] = React.useState("none")

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
            <Card order="card_first" cardClass="card_yes"/>
            <Card order="card_second" cardClass="card_no"/>
        </div>
    )
}

CardStack.propTypes = {

}

export default CardStack

