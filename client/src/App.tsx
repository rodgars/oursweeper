import React from "react"
import { useNavigate } from "react-router-dom"
import logo from "./logo.jpeg"
import "./App.css"

function App() {
	let navigate = useNavigate()

	const handleNewGame = async (difficulty: string) => {
		const difficultyMap: {
			[key: string]: { rows: number; columns: number; mines: number }
		} = {
			easy: { rows: 9, columns: 9, mines: 10 },
			medium: { rows: 16, columns: 16, mines: 40 },
			hard: { rows: 24, columns: 24, mines: 99 },
		}

		const payload = difficultyMap[difficulty]

		const response = await fetch(`http://localhost:5000/game/new`, {
			method: "POST",
			body: JSON.stringify(payload),
			headers: {
				"Content-Type": "application/json",
			},
		})
		const data = await response.json()

		navigate(`/game/${data.code}`)
	}

	return (
		<div className="App">
			<img src={logo} alt="logo" />
			<p className="game-slogan">
				Can you uncover all the mines without triggering a blast?
			</p>
			<fieldset className="game-box">
				<legend>Create a Game</legend>
				<div className="button-container">
					<button className="game-button" onClick={() => handleNewGame("easy")}>
						Easy
					</button>
					<button
						className="game-button"
						onClick={() => handleNewGame("medium")}
					>
						Medium
					</button>
					<button className="game-button" onClick={() => handleNewGame("hard")}>
						Hard
					</button>
				</div>
			</fieldset>
		</div>
	)
}

export default App
