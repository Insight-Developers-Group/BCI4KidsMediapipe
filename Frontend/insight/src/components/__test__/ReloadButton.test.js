import { fireEvent, render, screen } from '@testing-library/react';
import ReloadButton from '../ReloadButton';

it('should render the reload icon', () => {
    render(<ReloadButton />);
    const ReloadButtonIcon = screen.getByAltText(/reload-icon/i);
    expect(ReloadButtonIcon.getAttribute("src")).toMatch(new RegExp('reloadlogo.svg'));
});

it('should render the reload button background', () => {
    render(<ReloadButton />);
    const ReloadButtonBackground = screen.getByTestId("reloadIconBgrnd")
    expect(ReloadButtonBackground).toBeInTheDocument();
});

it('should reload when clicked', () => {
    const consoleSpy = jest.spyOn(console, 'log');
    render(<ReloadButton />);
    fireEvent.click(screen.getByTestId("reloadIconBgrnd"))
    expect(consoleSpy).toHaveBeenLastCalledWith("Reloaded")
});
