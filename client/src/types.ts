export interface CellContent {
	row: number
	column: number
	is_mine: boolean
	is_revealed: boolean
	is_flagged: boolean
	adjacent_mines: number
}

export interface GameMapState {
	map: CellContent[][]
	state: string
	code: string
	started_at: string
	total_time_in_seconds: number
}
