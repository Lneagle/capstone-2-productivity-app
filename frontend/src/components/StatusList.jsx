function StatusList({ teammates, setTeammates }) {
  const priorityMapping = {
    'High': '🔴',
    'Medium': '🟡',
    'Low': '🟢'
  };

  const statuses = teammates.map(person => {
    const statusObj = {};
    statusObj.name = person.name;
    statusObj.task = "free";
    statusObj.priority = 'Low';
    person.time_entries.forEach(entry => {
      if (entry.end_time == null) {
        statusObj.task = entry.task.name;
        statusObj.priority = entry.task.priority;
      }
    })
    return statusObj;
  });

  const teamList = statuses.map(person => 
    <li key={person.id}>
      <h4><span className={person.priority}>&#9679;</span> {person.name}</h4>
      {person.task}
    </li>
  );

	return (
		<ul className="status-list">
      {teamList}
		</ul>
	)
}

export default StatusList;