import { useState, useEffect } from "react";
import NavBar from "../components/NavBar";
import TaskList from "../components/TaskList";
import StatusList from "../components/StatusList";
import { fetchOpenTimeEntry, fetchTeamTasks, fetchTeamUsers, fetchUserTasks } from "../services/fetchData";

function Dashboard() {
	const [isAdmin, setIsAdmin] = useState(false);
	const [tasks, setTasks] = useState([]);
  const [tasksLoading, setTasksLoading] = useState(true);
  const [tasksError, setTasksError] = useState(null);
	const [openTaskId, setOpenTaskId] = useState(null);
	const [openEntryId, setOpenEntryId] = useState(null);
	const [teammates, setTeammates] = useState([]);
  const [teamLoading, setTeamLoading] = useState(true);
  const [teamError, setTeamError] = useState(null);

	useEffect(() => {
    const getTasks = async () => {
      try {
				let data;
				if (isAdmin) {
					data = await fetchTeamTasks();
				} else {
	        data = await fetchUserTasks();
				}
        setTasks(data);
      } catch (err) {
        setTasksError(err);
      } finally {
        setTasksLoading(false);
      }
    };

    getTasks();
  }, [isAdmin]);

	useEffect(() => {
    const getOpenTask = async () => {
      try {
        const data = await fetchOpenTimeEntry();
        setOpenTaskId(data.task_id);
				setOpenEntryId(data.entry_id);
      } catch (err) {
				console.log(err);
        setOpenTaskId(null);
				setOpenEntryId(null)
      }
    };

    getOpenTask();
  }, []);

	useEffect(() => {
    const getTeam = async () => {
      try {
        const data = await fetchTeamUsers();
        setTeammates(data);
      } catch (err) {
        setTeamError(err);
      } finally {
        setTeamLoading(false);
      }
    };

    getTeam();
  }, []);

	const handleToggle = (event) => {
		setIsAdmin(!isAdmin);
	}

	return (
		<>
			<NavBar />
			<div className="admin-toggle">
				<label htmlFor="admin">Admin mode:</label>
				<input type="checkbox" id="admin" onChange={handleToggle} />
			</div>
			<main className="flex">
				<section>
					{tasksLoading && <p>Loading tasks...</p>}
					{tasksError && <p>Error: {tasksError.message}</p>}
					<TaskList tasks={tasks} setTasks={setTasks} openTaskId={openTaskId} openEntryId={openEntryId} teammates={teammates} isAdmin={isAdmin} />
				</section>
				<section className="team-status">
					{teamLoading && <p>Loading team statuses...</p>}
					{teamError && <p>Error: {teamError.message}</p>}
        	<StatusList teammates={teammates} setTeammates={setTeammates}/>
				</section>
			</main>
		</>
	)
}

export default Dashboard;