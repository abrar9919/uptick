import {useState} from "react"
import DatePicker from "react-datepicker"
import "react-datepicker/dist/react-datepicker.css"
import {Box, Button, OutlinedInput} from "@mui/material"

function App() {
	const [startDate, setStartDate] = useState(new Date())
	const [endDate, setEndDate] = useState(new Date())
	const [ticker, setTicker] = useState("")
	const [tickerData, setTickerData] = useState([])
	const fetchTicker = async () => {
		console.log("Fetch Ticker being called")
		try {
			const response = await fetch(
				`http://127.0.0.1:8000/get-ticker?ticker=${ticker}&from_date=${startDate.getFullYear()}-${
					startDate.getMonth() + 1
				}-${startDate.getDate()}&to_date=${endDate.getFullYear()}-${
					endDate.getMonth() + 1
				}-${endDate.getDate()}`
			)
			const data = await response.json()
			setTickerData(data)
		} catch (e) {
			throw new Error("Something went wrong")
		}
	}
	console.log(tickerData)

	return (
		<Box p='2rem'>
			<h1>Search for a ticker to get started</h1>
			<Box display='flex' py='1rem'>
				<OutlinedInput
					onChange={(e) => setTicker(e.target.value)}
					value={ticker}
				/>
			</Box>
			<p>From:</p>

			<DatePicker
				selected={startDate}
				onChange={(date) => {
					if (date) setStartDate(date)
				}}
			/>
			<p>To:</p>
			<DatePicker
				selected={endDate}
				onChange={(date) => {
					if (date) setEndDate(date)
				}}
			/>
			<Box display='flex' pt='2rem'>
				<Button variant='contained' onClick={() => fetchTicker()}>
					Submit
				</Button>
			</Box>
			{Array.isArray(tickerData?.data) && (
				<table>
					<thead>
						<tr>
							<td>High</td>
							<td>Low</td>
							<td>Close</td>
							<td>Volume</td>
							<td>Date</td>
						</tr>
					</thead>
					<tbody>
						{tickerData?.data.map((data) => (
							<tr key={data.date}>
								<td>{data.high}</td>
								<td>{data.low}</td>
								<td>{data.close}</td>
								<td>{data.volume}</td>
								<td>{data.date}</td>
							</tr>
						))}
					</tbody>
				</table>
			)}
		</Box>
	)
}

export default App
