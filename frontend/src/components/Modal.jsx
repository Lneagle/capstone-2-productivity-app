import { useState } from "react";

function Modal({ setIsEditMode, projects, showProjects, task, teammates, onSubmit }) {
  const [taskName, setTaskName] = useState(task ? task.name : '');
  const [project, setProject] = useState('');
  const [priority, setPriority] = useState(task ? task.priority : '');
  const [assignee, setAssignee] = useState((task && task.assignee) ? task.assignee.id : '');
  const [isValidationError, setIsValidationError] = useState(false);

  const handleClose = () => {
    setIsEditMode(false);
  }

  const handleNameChange = (event) => {
    if (isValidationError) {
      setIsValidationError(false);
    }
    setTaskName(event.target.value);
  }
  
  const handleProjectChange = (event) => {
    if (isValidationError) {
      setIsValidationError(false);
    }
    setProject(event.target.value);
  }

  const handlePriorityChange = (event) => {
    if (isValidationError) {
      setIsValidationError(false);
    }
    setPriority(event.target.value);
  }

  const handleAssigneeChange = (event) => {
    setAssignee(event.target.value);
  }

  const handleFormSubmit = (event) => {
    event.preventDefault();
    if (!taskName || (showProjects && !project) || !priority) {
      setIsValidationError(true);
    } else {
      const data = JSON.stringify({
        "name": taskName,
        "priority": priority,
        "assignee_id": assignee
      });
      onSubmit(task, data, project);
      setTaskName('');
      setProject('');
      setAssignee('');
      setPriority('Low');
      handleClose();
    }
  }

	return (
		<div className="modal-container">
      <div className="modal">
        
        <form onSubmit={handleFormSubmit}>
          <div className="form-group">
            <button className="close" onClick={handleClose}>X</button>
            <label htmlFor="taskName">Task Name:</label>
            <input type="text" id="taskName" value={taskName} onChange={handleNameChange} />
          </div>
          {showProjects &&
            <div className="form-group">
              <label htmlFor="project">Project:</label>
              <select id="project" value={project} onChange={handleProjectChange}>
                <option value="">-- Choose project --</option>
                {projects.map(p => (
                  <option key={p.id} value={p.id}>{p.client.name} - {p.name}</option>
                ))}
              </select>
            </div>
          }
          <div className="form-group">
            <label htmlFor="priority">Priority:</label>
            <select id="priority" value={priority} onChange={handlePriorityChange}>
              <option value="">-- Choose priority --</option>
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
            </select>
          </div>
          <div className="form-group">
            <label htmlFor="assignee">Assignee:</label>
            <select id="assignee" value={assignee} onChange={handleAssigneeChange}>
              <option value="">None</option>
              {teammates.map(person => (
                <option key={person.id} value={person.id}>{person.name}</option>
              ))}
            </select>
          </div>
          {isValidationError && <p className="error">Task Name, Project, and Priority cannot be empty</p>}
          <input type="submit" value="Submit" />
        </form>
      </div>
		</div>
	)
}

export default Modal;