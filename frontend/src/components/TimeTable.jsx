function TimeTable({ entries }) {
  const timeAggregate = {};
  const timeByDate = {};
  const inProgress = [];
  const headingDates = [];

  headingDates.push('Total');

  for (let i = 0; i < 7; i++) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    headingDates.unshift((d.getMonth() + 1) + '-' + d.getDate()); 
  }

  function secondsToTime(time) {
    const dateObj = new Date(time);
    const hours = dateObj.getUTCHours();
    let minutes = dateObj.getUTCMinutes();
    const seconds = dateObj.getSeconds();
    if (seconds > 30) {
      minutes++;
    }
    const hourString = hours ? hours.toString() + 'h' : ''
    return hourString + minutes.toString() + 'm';
  }

  entries.forEach(entry => {
    if (entry.start_time && entry.end_time) {
      const clientName = entry.task.project.client.name;
      const projectName = entry.task.project.name;
      const taskName = entry.task.name;
      const date = entry.start_time.substring(5, 10).replace(/(^|-)0/g, '$1');
      if (!timeAggregate[clientName]) {
        timeAggregate[clientName] = {};
      }
      if (!timeAggregate[clientName][projectName]) {
        timeAggregate[clientName][projectName] = {};
      }
      if (!timeAggregate[clientName][projectName][taskName]) {
        timeAggregate[clientName][projectName][taskName] = {};
        timeAggregate[clientName][projectName][taskName]['Total'] = 0;
      }
      if (!timeAggregate[clientName][projectName][taskName][date]) {
        timeAggregate[clientName][projectName][taskName][date] = 0;
      }
      if (!timeByDate[date]) {
        timeByDate[date] = 0;
      }

      const entryTime = Date.parse(entry.end_time) - Date.parse(entry.start_time);
      timeAggregate[clientName][projectName][taskName][date] += entryTime;
      timeAggregate[clientName][projectName][taskName]['Total'] += entryTime;
      timeByDate[date] += entryTime;
    } else {
      inProgress.push(entry);
    }
  })

  const timeList = [];

  Object.entries(timeAggregate).forEach(([clientName, clientObj]) => {
    timeList.push(
      <tr key={`client-${clientName}`}>
        <th className="client" colSpan={headingDates.length + 1}>{clientName}</th>
      </tr>);
    
    Object.entries(clientObj).forEach(([projectName, projectObj]) => {
      timeList.push(
        <tr key={`project-${clientName}-${projectName}`}>
          <th className="project" colSpan={headingDates.length + 1}>{projectName}</th>
        </tr>
      );
      
      Object.entries(projectObj).forEach(([taskName, taskObj]) => {
        timeList.push(
          <tr key={`task-${clientName}-${projectName}-${taskName}`}>
            <th className="task">{taskName}</th>
            {headingDates.map(date =>
              <td key={`${taskName}-${date}`}>{taskObj[date] ? secondsToTime(taskObj[date]) : ''}</td>
            )}
          </tr>
        );
      });
    });
  });

  timeList.push(
    <tr key={'total-row'}>
      <th className="client">Total</th>
      {headingDates.map(date =>
        <td key={`total-${date}`}>{timeByDate[date] ? secondsToTime(timeByDate[date]) : ''}</td>
      )}
    </tr>
  )

	return (
		<>
      <table className="timetable">
        <thead>
          <tr>
            <th></th>
            {headingDates.map(date => <th key={date}>{date}</th>)}
          </tr>
        </thead>
        <tbody>
          {timeList}
        </tbody>
      </table>
		</>
	)
}

export default TimeTable;