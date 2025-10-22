import { useState, useEffect } from "react";
import NavBar from "../components/NavBar";
import TaskList from "../components/TaskList";
import StatusList from "../components/StatusList";
import { fetchUserTasks } from "../services/fetchData";

function Dashboard() {
	const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

	useEffect(() => {
    const getTasks = async () => {
      try {
        const data = await fetchUserTasks();
        setTasks(data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    getTasks();
  }, []);

  if (loading) return <p>Loading task...</p>;
  if (error) return <p>Error: {error.message}</p>;

	return (
		<>
			<NavBar />
			<main>
				<TaskList tasks={tasks} setTasks={setTasks} />
        <StatusList />
			</main>
		</>
	)
}

export default Dashboard;