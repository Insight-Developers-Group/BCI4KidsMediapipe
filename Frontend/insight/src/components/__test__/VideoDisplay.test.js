import { fireEvent, render, screen } from '@testing-library/react';
import VideoDisplay from '../VideoDisplay';

it('should render the card stack', () => {
    render(<VideoDisplay />);
    const Vid = screen.getByTestId("video-display")
    expect(Vid).toBeInTheDocument();
});
