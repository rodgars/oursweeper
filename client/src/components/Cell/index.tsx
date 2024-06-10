import React, { useContext } from "react"
import GameContext from "../../contexts/GameContext"

import "./style.css"
import { CellContent } from "../../types"

const Cell = ({
	value,
	is_game_finished,
}: {
	value: CellContent
	is_game_finished: boolean
}) => {
	const { handleCellClick, handleFlipFlag } = useContext(GameContext) || {}

	const getValueToDisplay = (value: CellContent) => {
		const { is_revealed, is_flagged, is_mine } = value

		if (is_game_finished && is_mine && !is_flagged) {
			return "💣"
		}

		if (!is_revealed) {
			return is_flagged ? "🚧" : ""
		}

		return value.adjacent_mines > 0 ? value.adjacent_mines : ""
	}

	const getClassName = (value: CellContent) => {
		const { is_revealed, is_flagged, is_mine } = value

		const is_empty = value.adjacent_mines === 0 && !is_mine

		const cellClass =
			"cell" +
			(is_revealed ? "" : " hidden") +
			(is_mine ? " is-mine" : "") +
			(is_empty ? " is_empty" : "") +
			(is_flagged ? " is-flag" : "")

		return cellClass
	}

	const handleClick = () => {
		const { row, column, is_revealed, is_flagged } = value
		if (is_game_finished || !handleCellClick || is_revealed || is_flagged)
			return
		handleCellClick(row, column)
	}

	const handleRightClick = (event: React.MouseEvent) => {
		event.preventDefault()
		const { row, column, is_revealed } = value
		if (is_game_finished || !handleFlipFlag || is_revealed) return
		handleFlipFlag(row, column)
	}

	return (
		<div
			className={getClassName(value)}
			onClick={handleClick}
			onContextMenu={handleRightClick}
		>
			{getValueToDisplay(value)}
		</div>
	)
}

export default Cell
