import React from 'react'
import PropTypes from 'prop-types'

function Card(props) {

    var cardLabel = ""
    switch (props.cardClass) {
        case "card_yes":
            cardLabel = "YES"
            break;

        case "card_no":
            cardLabel = "NO"
            break;
    
        default:
            cardLabel = ""
            break;
    }

    return (
        <div className={ 'card ' + props.cardClass + ' ' + props.order }>
            <h3 className="card_label">{cardLabel}</h3>
        </div>
    )
}

Card.propTypes = {

}

export default Card

