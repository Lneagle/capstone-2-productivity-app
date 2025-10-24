import { useState, useEffect } from "react";
import NavBar from "../components/NavBar";
import TimeTable from "../components/TimeTable";
import { fetchTimeEntries, fetchTeamUsers } from "../services/fetchData";

function TimeSheet() {
	const isAdmin = false; // replace
	const [userId, setUserId] = useState(1); //
	const [entries, setEntries] = useState([]);
	const [teammates, setTeammates] = useState([]);
	const [loading, setLoading] = useState(true);
	const [entryError, setEntryError] = useState(null);
	const [teamError, setTeamError] = useState(null);

	useEffect(() => {
		const getEntries = async () => {
			try {
				const data = await fetchTimeEntries(userId);
				setEntries(data);
				setEntryError(null);
			} catch (err) {
				setEntryError(err);
			} finally {
				setLoading(false);
			}
		};

		getEntries();
	}, [userId]);

	useEffect(() => {
		if (isAdmin) {
			const getTeam = async () => {
				try {
					const data = await fetchTeamUsers();
					setTeammates(data);
				} catch (err) {
					setTeamError(err);
				}
			};
	
			getTeam();
		};
	}, [isAdmin]);

	const handleSubmit = (event) => {
		event.preventDefault();
	}

	const handleUserChange = (event) => {
		setUserId(event.target.value);
	}

	return (
		<>
      <NavBar />
			{isAdmin && 
				<form onSubmit={handleSubmit}>
					<label htmlFor="user-select">Team Member:</label>
					<select id="user-select" value={userId} onChange={handleUserChange}>
						{teammates.map((person) => (
							<option key={person.id} value={person.id}>{person.name}</option>
						))}
					</select>
				</form>
			}
			{loading && <p>Loading timesheet...</p>}
			{entryError && <p>Error: {entryError.message}</p>}
			{teamError && <p>Error: {teamError.message}</p>}
			{!entryError && <TimeTable entries={entries} /> }
		</>
	)
}

export default TimeSheet;