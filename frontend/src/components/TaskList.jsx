import { useState } from "react";

function TaskList({ tasks }) {
  const sortedTasks = [...tasks];
  const isAdmin = false; //replace with cookie later
  const [enabledId, setEnabledId] = useState(null);
  const [isStartDisabled, setIsStartDisabled] = useState(false)

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

  const startTask = (id) => {
    setEnabledId(id);
    setIsStartDisabled(true);
  }

  const stopTask = (id) => {
    setEnabledId(null);
    setIsStartDisabled(false);
  }

  const taskList = sortedTasks.map(task =>
		<tr key={task.id}>
			<td>{task.project.client.name}</td>
			<td>{task.project.name}</td>
			<td>{task.name}</td>
			<td>{task.priority}</td>
      {isAdmin ? <td></td> : ''}
			<td>{task.completed ? '✓' : ''}</td>
			<td>{isAdmin ? <button onClick={() => editTask(task.id)}>Edit</button> : <button onClick={() => startTask(task.id)} disabled={isStartDisabled}>Start</button>}</td>
			<td>{isAdmin ? <button onClick={() => deleteTask(task.id)}>Delete</button> : <button onClick={() => stopTask(task.id)} disabled={task.id != enabledId}>Stop</button>}</td>
		</tr>
	);

	return (
		<>
      <table>
				<thead>
					<tr>
						<th>Client</th>
						<th>Project</th>
						<th>Task Name</th>
						<th>Priority</th>
            {isAdmin ? <th>Assignee</th>: ''}
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