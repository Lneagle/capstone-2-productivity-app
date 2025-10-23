import { useState, useRef } from "react";
import { createTimeEntry, endTimeEntry, patchTask } from "../services/fetchData";

function TaskList({ tasks, setTasks, openTaskId, openEntryId }) {
  console.log(openTaskId, openEntryId);
  const sortedTasks = [...tasks];
  const isAdmin = false; //replace with cookie later
  const [enabledId, setEnabledId] = useState(openTaskId);
  console.log(enabledId)
  const [isStartDisabled, setIsStartDisabled] = useState(openTaskId)
  const [error, setError] = useState(null);
  const entryId = useRef(openEntryId);
  console.log(entryId.current)

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

  const postEntry = async (task_id) => {
    try {
      const data = await createTimeEntry(task_id);
      entryId.current = data.id;
    } catch (err) {
      setError(err);
    }
  };

  const endEntry = async (task_id) => {
    try {
      const data = await endTimeEntry(entryId.current);
      entryId.current = null;
    } catch (err) {
      setError(err);
    }
  };

  const startTask = (task_id) => {
    setEnabledId(task_id);
    setIsStartDisabled(true);
    postEntry(task_id);
  };

  const stopTask = (task_id) => {
    setEnabledId(null);
    setIsStartDisabled(false);
    endEntry(task_id);
  };

  const completeTask = async (client_id, project_id, task_id) => {
    try {
      const data = await patchTask(client_id, project_id, task_id, JSON.stringify({"completed": true}));
      sortedTasks.forEach(task => {
        if (task.id == data.id) {
          task.completed = data.completed;
        }
      })
      setTasks(sortedTasks);
    } catch (err) {
      setError(err);
    }
  };

  const taskList = sortedTasks.map(task =>
		<tr key={task.id}>
			<td>{task.project.client.name}</td>
			<td>{task.project.name}</td>
			<td>{task.name}</td>
			<td>{task.priority}</td>
      {isAdmin && <td></td>}
			<td>{task.completed ? '✓' : <button onClick={() => completeTask(task.project.client.id, task.project.id, task.id)}>Mark Completed</button>}</td>
			<td>{isAdmin ? <button onClick={() => editTask(task.id)}>Edit</button> : <button onClick={() => startTask(task.id)} disabled={isStartDisabled || task.completed}>Start</button>}</td>
			<td>{isAdmin ? <button onClick={() => deleteTask(task.id)}>Delete</button> : <button onClick={() => stopTask(task.id)} disabled={task.id != enabledId}>Stop</button>}</td>
		</tr>
	);

	return (
		<>
      {error && <p>Error: {error.message}</p>}
      <table>
				<thead>
					<tr>
						<th>Client</th>
						<th>Project</th>
						<th>Task Name</th>
						<th>Priority</th>
            {isAdmin && <th>Assignee</th>}
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