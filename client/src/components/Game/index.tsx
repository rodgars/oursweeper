import React, { useEffect, useState, useRef } from "react"
import { useParams } from "react-router-dom"
import Board from "../Board"
import { GameMapState } from "../../types"

import "./style.css"
import GameContext, { GameContextType } from "../../contexts/GameContext"

const Game = () => {
	const { code } = useParams()
	const [gameData, setGameData] = useState<GameMapState | null>(null)
	const [username, setUsername] = useState<string | null>(null)
	const [isWsConnected, setIsWsConnected] = useState<boolean>(false)
	const [usersConnected, setUsersConnected] = useState<string[]>([])

	const ws = useRef<WebSocket | null>(null)

	useEffect(() => {
		if (!username || !code) return

		// Connect to the WebSocket server
		ws.current = new WebSocket(
			`ws://localhost:5000/ws/game/${code}/?user=${username}`,
		)

		// Handle incoming messages
		ws.current.onmessage = (event) => {
			const data = JSON.parse(event.data)

			const messageType = data["type"]

			if (messageType === "update.map") {
				const gameMap = data["map"]
				setGameData(gameMap)
			} else if (messageType === "user.list") {
				setUsersConnected(data["users"])
			}
		}

		// Send a message when the connection is opened
		ws.current.onopen = () => {
			setIsWsConnected(true)
		}

		// Clean up the WebSocket connection when the component unmounts
		return () => {
			ws.current?.close()
		}
	}, [code, username])

	useEffect(() => {
		const key = "username"
		let storedValue = localStorage.getItem(key)
		if (!storedValue) {
			storedValue = window.prompt("Please enter your username")
			if (storedValue) {
				localStorage.setItem(key, storedValue)
			}
		}
		setUsername(storedValue)
	}, [])

	useEffect(() => {
		if (!username || !code) return

		async function fetchGame() {
			const resp = await fetch(`http://localhost:5000/game/${code}`)
			const data = await resp.json()
			setGameData(data)
		}
		fetchGame()
	}, [code, setGameData, username])

	const handleCellClick = async (row: number, col: number) => {
		if (!ws.current) return
		const payload = { row, column: col, user: username, type: "reveal" }
		ws.current.send(JSON.stringify(payload))

		// --- To be removed --- Use this code to make a POST request instead of using WebSocket
		// const payload = { row, column: col }
		// const resp = await fetch(`http://localhost:5000/game/${code}/move`, {
		// 	method: "POST",
		// 	body: JSON.stringify(payload),
		// 	headers: {
		// 		"Content-Type": "application/json",
		// 	},
		// })
		// if (resp.ok) {
		//     const data = await resp.json()
		//     setGameData(data)
		// }
	}

	const handleFlipFlag = async (row: number, col: number) => {
		if (!ws.current) return
		const payload = { row, column: col, user: username, type: "flag" }
		ws.current.send(JSON.stringify(payload))

		// --- To be removed --- Use this code to make a POST request instead of using WebSocket
		// const payload = { row, column: col }
		// const resp = await fetch(`http://localhost:5000/game/${code}/flip_flag`, {
		// 	method: "POST",
		// 	body: JSON.stringify(payload),
		// 	headers: {
		// 		"Content-Type": "application/json",
		// 	},
		// })
		// if (resp.ok) {
		//     const data = await resp.json()
		//     setGameData(data)
		// }
	}

	const contextValue: GameContextType = {
		handleCellClick,
		handleFlipFlag,
	}

	return (
		<div className="game">
			{gameData && username && isWsConnected && (
				<GameContext.Provider value={contextValue}>
					<Board
						gameMap={gameData}
						username={username}
						users={usersConnected}
					/>
				</GameContext.Provider>
			)}
		</div>
	)
}

export default Game
