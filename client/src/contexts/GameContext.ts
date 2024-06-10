import React from "react"

export interface GameContextType {
	handleCellClick: (row: number, col: number) => void
	handleFlipFlag: (row: number, col: number) => void
}

const GameContext = React.createContext<GameContextType | null>(null)

export default GameContext
