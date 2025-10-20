import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import TimeSheet from './pages/Timesheet';

const App = () => (
  <BrowserRouter>
      <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/timesheet" element={<TimeSheet />} />
      </Routes>
  </BrowserRouter>
  )

export default App
