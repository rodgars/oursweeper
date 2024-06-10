import React from "react"
import { render, screen } from "@testing-library/react"
import App from "./App"

test("renders fieldset with legend", () => {
	render(<App />)
	const legendElement = screen.getByText(/Create a Game/i)
	expect(legendElement).toBeInTheDocument()
})
