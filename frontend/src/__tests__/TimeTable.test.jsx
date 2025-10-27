import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor, within } from '@testing-library/react'
import TimeTable from '../components/TimeTable'

describe('TimeTable', () => {
  it('renders without crashing', () => {
    render(<TimeTable entries={[]} />);
  });
  
  it('displays time entries correctly', () => {
    const mockEntries = [
      {
        start_time: '2025-10-20T09:00:00',
        end_time: '2025-10-20T10:30:00',
        task: {
          name: 'Development',
          project: {
            name: 'Website',
            client: { name: 'Acme Corp' }
          }
        }
      }
    ];
    
    render(<TimeTable entries={mockEntries} />);
    expect(screen.getByText('Acme Corp')).toBeInTheDocument();
  });
});
