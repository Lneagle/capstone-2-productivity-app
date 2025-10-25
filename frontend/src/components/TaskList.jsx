import { useState, useRef } from "react";
import { createTimeEntry, endTimeEntry, fetchTeamProjects, patchTask, postTask, deleteTask } from "../services/fetchData";
import Modal from "./Modal";

function TaskList({ tasks, setTasks, openTaskId, openEntryId, teammates, isAdmin }) {
  //console.log(openTaskId, openEntryId);
  const sortedTasks = [...tasks];
  const [enabledId, setEnabledId] = useState(openTaskId);
  //console.log(enabledId);
  const [isStartDisabled, setIsStartDisabled] = useState(openTaskId)
  const [error, setError] = useState(null);
  const entryId = useRef(openEntryId);
  //console.log(entryId.current);
  const [projects, setProjects] = useState([]);
  const [showProjects, setShowProjects] = useState(false);
  const [isEditMode, setIsEditMode] = useState(false);
  const [taskToEdit, setTaskToEdit] = useState(null);

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

  const getProjects = async () => {
    try {
      const data = await fetchTeamProjects();
      data.sort((a, b) => {
        if (a.client.name < b.client.name) {
          return -1;
        } else if (a.client.name > b.client.name) {
          return 1;
        } else if (a.name < b.name) {
          return -1;
        } else if (a.name > b.name) {
          return 1;
        } else {
          return 0;
        }
      });
      setProjects(data);
    } catch (err) {
      setError(err);
    }
  }

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

  const addTask = () => {
    setTaskToEdit(null);
    if (projects.length == 0) {
      getProjects();
    }
    setShowProjects(true);
    setIsEditMode(true);
  }

  const editTask = (task) => {
    setIsEditMode(true);
    setShowProjects(false);
    setTaskToEdit(task);
  }

  const removeTask = async (task) => {
    try {
      await deleteTask(task.project.client.id, task.project.id, task.id);
      setTasks(sortedTasks.filter(t => {return t.id != task.id}));
    } catch (err) {
      setError(err);
    }
  }

  const handleSubmit = async (task, data, project) => {
    if (task) {
      try {
        const updatedTask = await patchTask(task.project.client.id, task.project.id, task.id, data);
        setTasks(sortedTasks.map(task => {
          return task.id == updatedTask.id ? updatedTask : task;
        }));
        setTaskToEdit(null);
      } catch (err) {
        setError(err);
      }
    } else {
      try {
        const newTask = await postTask(project, data);
        setTasks([...sortedTasks, newTask]);
      } catch (err) {
        setError(err);
      }
    }
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
      {isAdmin && <td>{task.assignee ? task.assignee.name : ''}</td>}
			<td className="completed">{task.completed ? '✓' : <input type="checkbox" onClick={() => completeTask(task.project.client.id, task.project.id, task.id)} />}</td>
			<td>{isAdmin ? <button onClick={() => editTask(task)}>Edit</button> : <button onClick={() => startTask(task.id)} disabled={isStartDisabled || task.completed}>Start</button>}</td>
			<td>{isAdmin ? <button className="delete" onClick={() => removeTask(task)}>Delete</button> : <button onClick={() => stopTask(task.id)} disabled={task.id != enabledId}>Stop</button>}</td>
		</tr>
	);

	return (
		<>
      {error && <p className="error">Error: {error.message}</p>}
      <table >
				<thead>
					<tr>
						<th>Client</th>
						<th>Project</th>
						<th>Task Name</th>
						<th>Priority</th>
            {isAdmin && <th>Assignee</th>}
						<th>Completed</th>
						<th colSpan={2}><button className="add" onClick={() => addTask()}>Add Task</button></th>
					</tr>
				</thead>
				<tbody>
          {isAdmin &&
            <tr>
              <th></th>
              <th>{/* <button>Add Project</button> */}</th>
              <th></th>
              <th></th>
              <th></th>
              <th></th>
              <th></th>
              <th></th>
            </tr>
          }
					{taskList}
				</tbody>
			</table>
      {isEditMode && <Modal setIsEditMode={setIsEditMode} projects={projects} showProjects={showProjects} task={taskToEdit} teammates={teammates} onSubmit={handleSubmit}/>}
		</>
	)
}

export default TaskList;