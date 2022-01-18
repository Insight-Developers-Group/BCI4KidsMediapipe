import { fireEvent, render, screen } from '@testing-library/react';
import MenuButton from '../MenuButton';

it('should render the reload icon', () => {
    render(<MenuButton />);
    const menuBtn = screen.getByTestId('menu-btn');
    expect(menuBtn).toBeInTheDocument();
});

it('should open when clicked once, then close when clicked again', () => {
    const consoleSpy = jest.spyOn(console, 'log');
    render(<MenuButton />);
    fireEvent.click(screen.getByTestId("menu-btn"))
    expect(consoleSpy).toHaveBeenLastCalledWith("Menu Open")
    fireEvent.click(screen.getByTestId("menu-btn"))
    expect(consoleSpy).toHaveBeenLastCalledWith("Menu Closed")
});