import React from 'react'
import "./App.css";
const GameCard = ( {game} ) => {
    return(
        <div className='game'>
            <container>
                <div>
                    <p> {game.team1} {game.price1} <img src={game.book1 + ".png"} width="20" height="20" /> </p>
                    <p> {game.team2} {game.price2} <img src={game.book2 + ".png"} width="20" height="20" /> </p> 
                </div>
            </container>
        </div>
)
}

export default GameCard