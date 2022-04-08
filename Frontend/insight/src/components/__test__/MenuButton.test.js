import { fireEvent, render, screen } from '@testing-library/react';
import MenuButton from '../MenuButton';

it('should render the reload icon', () => {
    render(<MenuButton />);
    const menuBtn = screen.getByTestId('menu-btn');
    expect(menuBtn).toBeInTheDocument();
});

it('should open when clicked once, then close when clicked again', () => {
    render(<MenuButton />);
    const menuToggler = screen.getByTestId('menu-btn-toggler');
    const menuButton = screen.getByTestId('menu-btn');
    expect(menuButton).toHaveClass('menu-btn');
    fireEvent.click(menuToggler);
    expect(menuButton).toHaveClass('menu-btn-open');
    fireEvent.click(menuToggler);
    expect(menuButton).toHaveClass('menu-btn');
});