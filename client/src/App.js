import React, { useState, useEffect } from 'react'
import GameCard from './gameCard'
import "./App.css";
import NeatContainer from './neatContainer';
//this was between the div tags
//{(typeof data.members == 'undefined') ? ( //data.members
//<p>Loading...</p>
//) : (
//  data.members.map((member, i ) => ( //sample json data starts like that 
//    <p key={i}>{member}</p>
//  ))
//)}

const randomGame = 
  {
    "book1": "DraftKings",
    "team1": "Los Angeles Kings",
    "spread1": -3.5,
    "price1": -135,
    "book2": "DraftKings",
    "team2": "San Jose Sharks",
    "spread2": 3.5,
    "price2": 105,
    "isArb": false
  }

const Game = (props) => {
  return (
    <>
      <h1>{props.team1} vs {props.team2}</h1>
      <h2>{props.book1} and {props.book2}</h2>

    </>
  )
}


function App() {

  const [data , setData] = useState([{}])

  useEffect(() => {
    fetch("/arbs").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  },[])

  //const[leagueData, setLeague] = useState('icehockey_nhl') //use this to interchange api calls for what league
/*
    <div className='app'>
      <h1>Welcome to BettingFriend!</h1>
      <h2>Pick a league to see live betting lines</h2>
      <button>NHL</button>
      <button>NFL</button>
      <button>NBA</button>
      <button>MLB</button>

      {data.map((game) => (
      <>
      <container> <GameCard game= {game} /> </container>
      </>

      )
      )}

*/
  return (

    <div class='app'>
        <h1>Welcome to BettingFriend!</h1>
        <h2>Pick a league to see live betting lines</h2>
          {data.map((game) => (
          <container> <NeatContainer game= {game} /> </container>
          )
          )}
    </div>
  )
}

export default App
