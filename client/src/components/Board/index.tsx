import React, { useState, useEffect } from "react"
import Cell from "../Cell"

import "./style.css"
import { GameMapState } from "../../types"
import UserList from "../UserList"

const Board = ({
	gameMap,
	username,
	users,
}: {
	gameMap: GameMapState
	username: string
	users: string[] | null
}) => {
	const [seconds, setSeconds] = useState(gameMap.total_time_in_seconds)

	useEffect(() => {
		let interval: NodeJS.Timeout

		if (gameMap.state === "ongoing") {
			interval = setInterval(() => {
				setSeconds((seconds) => seconds + 1)
			}, 1000)
		}

		return () => clearInterval(interval)
	}, [gameMap.state])

	const formatTime = (seconds: number) => {
		const date = new Date(0)
		date.setSeconds(seconds)
		const timeString = date.toISOString().slice(11, 19)
		return timeString
	}

	const renderBoard = () => {
		const is_game_finished = gameMap.state !== "ongoing"
		return gameMap.map.map((row, r_i) => {
			const rowCells = row.map((cellValue, c_i) => (
				<Cell
					key={`${r_i}_${c_i}`}
					value={cellValue}
					is_game_finished={is_game_finished}
				/>
			))

			return (
				<div key={r_i} className="row">
					{rowCells}
				</div>
			)
		})
	}

	let gameStateMessage = "🔄 Game ongoing"
	if (gameMap.state === "won") gameStateMessage = "🏆 You won !"
	if (gameMap.state === "lost") gameStateMessage = "😱 You lost !"

	return (
		<div className="board">
			<div className="header">
				<div className="header-item">👋 Hello, {username}</div>
				<div className="header-item">
					⏰ <span>{formatTime(seconds)}</span>
				</div>
				<div className="header-item">{gameStateMessage}</div>
			</div>
			<div className="grid">{renderBoard()}</div>
			<UserList users={users} />
		</div>
	)
}

export default Board
