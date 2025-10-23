import { useState, useEffect } from "react";
import NavBar from "../components/NavBar";
import TimeTable from "../components/TimeTable";
import { fetchTimeEntries } from "../services/fetchData";

function TimeSheet() {
	const [entries, setEntries] = useState([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState(null);

	useEffect(() => {
		const getEntries = async () => {
			try {
				const data = await fetchTimeEntries();
				setEntries(data);
			} catch (err) {
				setError(err);
			} finally {
				setLoading(false);
			}
		};

		getEntries();
	}, []);

	return (
		<>
      <NavBar />
			<TimeTable entries={entries} />
		</>
	)
}

export default TimeSheet;