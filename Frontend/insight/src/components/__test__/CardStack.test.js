import { fireEvent, render, screen } from '@testing-library/react';
import CardStack from '../CardStack';

it('should render the card stack', () => {
    render(<CardStack />);
    const CardStk = screen.getByTestId("card_stack")
    expect(CardStk).toBeInTheDocument();
});
