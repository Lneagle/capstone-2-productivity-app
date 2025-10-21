import { useState, useEffect } from "react";
import { fetchUserTasks } from "../services/fetchData";

function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sortConfig, setSortConfig] = useState(null);

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

  const sortedTasks = [...tasks];

  sortedTasks.sort((a, b) => {
    const priorities = ["High", "Medium", "Low"]
    if (a.project.client.name < b.project.client.name) {
      return -1;
    } else if (a.project.client.name > b.project.client.name) {
      return 1;
    } else if (a.project.name < b.project.name) {
      return -1;
    } else if (a.project.name > b.project.name) {
      return 1;
    } else {
      return priorities.indexOf(a.priority) - priorities.indexOf(b.priority);
    }
  });

  const taskList = sortedTasks.map(task =>
		<tr key={task.id}>
			<td>{task.project.client.name}</td>
			<td>{task.project.name}</td>
			<td>{task.name}</td>
			<td>{task.priority}</td>
			<td>{task.completed ? '✓' : ''}</td>
			<td><button>Start</button></td>
			<td><button>Stop</button></td>
		</tr>
	);

  if (loading) return <p>Loading task...</p>;
  if (error) return <p>Error: {error.message}</p>;

	return (
		<>
      <table>
				<thead>
					<tr>
						<th>Client</th>
						<th>Project</th>
						<th>Task Name</th>
						<th>Priority</th>
						<th>Completed</th>
						<th></th>
						<th></th>
					</tr>
				</thead>
				<tbody>
					{taskList}
				</tbody>
			</table>
		</>
	)
}

export default TaskList;