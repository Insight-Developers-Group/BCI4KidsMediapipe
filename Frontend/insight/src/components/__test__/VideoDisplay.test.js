import { fireEvent, render, screen } from '@testing-library/react';
import VideoDisplay from '../VideoDisplay';

it('should render the video display component', () => {
    render(<VideoDisplay />);
    const Vid = screen.getByTestId("video-display")
    expect(Vid).toBeInTheDocument();
});

// TODO: Add tests for videoDisplay functionality